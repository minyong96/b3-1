from linkedlist import LinkedList


def main():
    print("ddd")
    data = 123
    new_linked_list = LinkedList(data)
    new_data = 213123
    new_linked_list.insert_back(new_data)
    
    new_data_front= 11111
    new_linked_list.insert_front(new_data_front)
    # new_linked_list.remove_back()
    # new_linked_list.remove_front()
    new_linked_list.get_nodes()


if __name__ == "__main__":
    main()