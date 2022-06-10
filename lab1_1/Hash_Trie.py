from building_dic import configure
Test_File = configure['Test_File']


#定义Trie结点的数据结构
class Node:
    def __init__(self, ending_flag=False, char='', list_len=70):
        self.char = char    # 字符
        self.cur_words = 0  # 统计当前子链的填充字符数
        self.child_list = [None] * list_len
        self.ending_flag = ending_flag  #终结符判断，True，表示叶子节点

    # 哈希函数（字符的Unicode编码值模子链的长度），得到字符的哈希值
    def hash_encoding(self, char):
        ans = ord(char) % len(self.child_list)
        return ans

    #插入子结点到其子链上
    def insert_child(self, child):
        if self.cur_words / float(len(self.child_list)) > float(3 / 4):  #当结点的子链的容量不足1/4的时候，对子节点进行扩容（2倍）
            self.cur_words = 0
            self.enlarge_size(child)
        id = self.hash_encoding(char=child.char) # 得到哈希编码
        while self.child_list[id] is not None:   #如果冲突，就寻找下一个位置
            id = (id + 1) % len(self.child_list)
        self.cur_words += 1
        self.child_list[id] = child  #插入子链

    #获取该字符的结点
    def get_node(self, char):
        id = self.hash_encoding(char)
        while True:
            child = self.child_list[id]
            if child is None:
                return None
            if child.char == char:
                return child
            id = (id + 1) % len(self.child_list)

    #扩大容量（增加为原来的两倍）
    def enlarge_size(self, child):
        old_child_list = self.child_list
        self.child_list = [None] * (2 * len(self.child_list))
        #拷贝旧链的字符到新的子链上
        for every_child in old_child_list:
            if every_child is not None:
                id = self.hash_encoding(char=every_child.char)
                while self.child_list[id] is not None:
                    id = (id + 1) % len(self.child_list)
                self.cur_words += 1
                self.child_list[id] = every_child
        self.insert_child(child)


#构造Trie（分别构造对应于FMM和BMM的Trie，二者的区别在于前者从一个单词的第一个字符开始，后者从一个单词的最后一个字符开始构造）
class Dic_Hash_Trie:
    Words_List = []

    @staticmethod
    def fmm_dic_root(dic_path='result_file/dic/dic.txt'):
        for line in open(dic_path, 'r', encoding='UTF-8'):
            Dic_Hash_Trie.Words_List.append(line.split()[0])
        root = Node(list_len=8000)
        for word in Dic_Hash_Trie.Words_List:
            Dic_Hash_Trie.insert_fmm(word, root)
        return root

    @staticmethod
    def bmm_dic_root(dic_path='result_file/dic/dic.txt'):
        for line in open(dic_path, 'r', encoding='UTF-8'):
            Dic_Hash_Trie.Words_List.append(line.split()[0])
        root = Node(list_len=8000)
        for word in Dic_Hash_Trie.Words_List:
            Dic_Hash_Trie.insert_bmm(word, root)
        return root

    @staticmethod
    #将一个单词word插入root中
    def insert_fmm(word, root):
        length = len(word)
        counter = 1
        node = root.get_node(word[0]) #获取单词中第一个字符的结点
        pre_node = root
        while node is not None:   #当Trie树的相应位置中存在该字符的结点时
            if counter == length:
                node.ending_flag = True
                return
            pre_node = node
            node = node.get_node(word[counter])
            counter += 1
        counter = counter - 1   #Trie树没有对应的该字符的节点，回到上一结点
        while counter < length:  #如果单词中还有字符，则创建新的字符结点
            node = Node()
            node.char = word[counter]
            counter += 1
            pre_node.insert_child(node)  #插入结点
            pre_node = node
        node.ending_flag = True    #终结符，表示叶子结点（一个单词的结尾）

    @staticmethod
    #以bmm的方式插入，即从一个单词最后一个字符开始插入
    def insert_bmm(word, root):
        counter = len(word) - 1
        node = root.get_node(word[counter])
        pre_node = root
        while node is not None:
            if counter == 0:
                node.ending_flag = True
                return
            counter -= 1
            pre_node = node
            node = node.get_node(word[counter])
        while counter >= 0:
            node = Node()
            node.char = word[counter]
            counter -= 1
            pre_node.insert_child(node)
            pre_node = node
        node.ending_flag = True
