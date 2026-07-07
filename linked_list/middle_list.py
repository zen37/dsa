from create_linked_list import build


# the classic slow/fast two-pointer ("tortoise and hare"), which does it in a single pass with no counting:
def middle_node_v2(head):
    # Time: O(n) single pass; Space: O(1)
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next  # moves 1 step
        fast = fast.next.next  # moves 2 steps
    return slow


# not so good solution, but it works and is easy to understand. It counts the number of nodes, then iterates again to find the middle node.
def middle_node_v1(head):
    # Time: O(n) + O(n) = O(n); Space: O(1)
    curr = head
    counter: int = 0

    while curr:
        counter += 1
        if curr.next == None and (counter == 1 or counter == 2):
            return curr
        curr = curr.next

    half: int = counter // 2
    counter = 0

    curr = head
    while curr:
        if half == counter:
            return curr
        curr = curr.next
        counter += 1


if __name__ == "__main__":
    # simple smoke test
    head = build([1, 2, 3, 4, 5])
    print(middle_node_v1(head).val)  # 3
    print(middle_node_v2(head).val)  # 3
