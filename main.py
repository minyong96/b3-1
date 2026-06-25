from data_structure.linked_list import DoublyLinkedList
from data_structure.hash_map import HashMap

def main():
    print("-----linkedlist-----")
    new_linked_list = DoublyLinkedList()
    new_data = 213123
    new_linked_list.insert_back(new_data)
    
    new_data_front= 11111
    new_linked_list.insert_front(new_data_front)
    
    for data in new_linked_list:
        print(data)
        



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