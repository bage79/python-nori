class Node(object):
    def __init__(self, key, data=None, result=None):
        self.key = key
        self.data = data
        # self.flag_ing = False
        # self.flag_end = False # whether or not leaf node
        self.result = []
        if result is not None:
            self.result.append(result)
        self.children = dict()


class Trie(object):
    """Trie Data Structure

    Data Structure for saving tokens with 
    morphologinal analysis results by Mecab-ko-dic
    """

    def __init__(self):
        self.head = Node(key=None)

    def insert(self, string, result):
        cur_node = self.head  # pivot

        for char_key in string:
            if char_key not in cur_node.children:
                cur_node.children[char_key] = Node(char_key)  # make node
            cur_node = cur_node.children[char_key]  # update pivot
            # cur_node.flag_end = False # re-init for new overlapping string, while iterating.
            # cur_node.flag_ing = True

        # now cur_node is leaf node
        # if len(cur_node.children) == 0: # leaf-node: not have child node
        #    cur_node.flag_end = True
        cur_node.data = string
        if result not in cur_node.result:
            cur_node.result.append(result)

    def search(self, string):
        cur_node = self.head

        for char_key in string:
            if char_key in cur_node.children:
                cur_node = cur_node.children[char_key]
            else:
                return (False, None)
                # return cur_node

        if cur_node.data is not None:
            return (True, cur_node)  # cur_node.result or cur_node.flag

        return (True, None)


if __name__ == "__main__":

    test_trie = Trie()

    token_list = ['자연어처리', '자연', '인공지능', '자', '자연어처리하자']

    token_info = dict()
    token_info['자연어처리'] = '[자연어처리 - 토큰 정보]'
    token_info['자연'] = '[자연 - 토큰 정보]'
    token_info['인공지능'] = '[인공지능 - 토큰 정보]'
    token_info['자'] = '[자 - 토큰 정보]'
    token_info['자연어처리하자'] = '[자연어처리하자 - 토큰 정보]'

    for token in token_list:
        test_trie.insert(token, token_info[token])

    ##
    for token in token_list:
        print(test_trie.search(token))
        print(test_trie.search(token).result)
        print(test_trie.search(token).flag)
        print('\n')
