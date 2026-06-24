from data_structure.linked_list import LinkedList
from data_structure.hash_map import HashMap

def main():
    print("-----linkedlist-----")
    data = 123
    new_linked_list = LinkedList(data)
    new_data = 213123
    new_linked_list.insert_back(new_data)
    
    new_data_front= 11111
    new_linked_list.insert_front(new_data_front)
    # new_linked_list.remove_back()
    # new_linked_list.remove_front()
    new_linked_list.get_nodes()
    result = new_linked_list.get_node(3)

    print(f"result : {result}")

    size = new_linked_list.get_size()
    print(f"size: {size}")



    print("------hashMap-------")

    hashMap = HashMap()
    size = hashMap.size()
    print(size)
    hashMap.put("apple", 23)
    hashMap.put("appl", 2693)
    hashMap.put("banananan", 2693)
    hashMap.put("banan", 2693) 
    value = hashMap.get("apple")
    size = hashMap.size()
    print(value)
    print(size)
    print([key for key in hashMap.keys()])
    hashMap.remove("banananan")
    print(hashMap.size())
    print([key for key in hashMap.keys()])



if __name__ == "__main__":
    main()