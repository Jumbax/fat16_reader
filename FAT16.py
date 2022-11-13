import struct


class FAT16:

    def __init__(self):
        with open('test.img', 'rb') as image:
            self.data = [int.to_bytes(byte) for byte in image.read()]
        self.directory_dict = {}
        self.get_data()
        self.read_root_dir()
        self.read_cluster_area()

    def get_data(self):
        self.reserved_sector = struct.unpack(
            '<H', b''.join(self.data[14:16]))[0]
        self.sector_size = struct.unpack('<H', b''.join(self.data[11:13]))[0]
        self.fat_size = struct.unpack('<H', b''.join(self.data[22:24]))[0]
        self.fat_copies = struct.unpack('B', self.data[16])[0]
        self.dir_entries = struct.unpack('<H', b''.join(self.data[17:19]))[0]
        self.cluster_size_in_sector = struct.unpack('B', self.data[13])[0]
        self.dir_entry_size = 32

    def get_root_dir_start(self):
        return (self.fat_size * self.fat_copies * self.sector_size * self.reserved_sector) + self.sector_size

    def get_cluster_area_start(self):
        return self.get_root_dir_start() + self.dir_entries * self.dir_entry_size

    def read_root_dir(self):
        for i in range(self.get_root_dir_start(), self.get_root_dir_start() + 4 * self.dir_entry_size, self.dir_entry_size):
            ascii_name = struct.unpack('B'*11, b''.join(self.data[i:i+11]))
            name = ''.join(chr(ascii) for ascii in ascii_name)
            self.directory_dict[name] = struct.unpack(
                '<H', b''.join(self.data[i+26:i+28]))[0]

    def read_cluster_area(self):
        for value in self.directory_dict:
            cluster_start = self.get_cluster_area_start(
            ) + (self.directory_dict[value] - 2) * (self.cluster_size_in_sector * self.sector_size)
            for i in range(cluster_start, cluster_start + (self.cluster_size_in_sector * self.sector_size), self.dir_entry_size):
                ascii_name = struct.unpack('B'*11, b''.join(self.data[i:i+11]))
                if (ascii_name == (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)):
                    break
                name = ''.join(chr(ascii) for ascii in ascii_name)
                print(value, name)


fat16 = FAT16()
