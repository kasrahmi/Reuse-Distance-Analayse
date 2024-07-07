import csv
import sys, os
import datetime
import numpy as np


class TreeNode:
    def __init__(self, content):
        self.content = content
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        self.subtree_size = 1


class Tree:
    def __init__(self):
        self.root = None
        self.node_map = {}  # Hash table to map content to tree nodes

    def insert(self, content):
        new_node = TreeNode(content)
        self.node_map[content] = new_node
        if self.root is None:
            self.root = new_node
        else:
            self._insert_left_most(new_node)
        self._update_size_and_height(new_node)
        self._balance_tree(new_node)

    def _insert_left_most(self, node):
        current = self.root
        while current.left is not None:
            current = current.left
        current.left = node
        node.parent = current

    def delete(self, content):
        if content not in self.node_map:
            raise ValueError("Content not found in the tree")
        node_to_delete = self.node_map[content]
        self._delete_node(node_to_delete)
        del self.node_map[content]

    def _delete_node(self, node):
        if node.left is None and node.right is None:
            if node.parent is None:
                self.root = None
            elif node == node.parent.left:
                node.parent.left = None
            else:
                node.parent.right = None
        elif node.left is None:
            if node.parent is None:
                self.root = node.right
                node.right.parent = None
            elif node == node.parent.left:
                node.parent.left = node.right
                node.right.parent = node.parent
            else:
                node.parent.right = node.right
                node.right.parent = node.parent
        elif node.right is None:
            if node.parent is None:
                self.root = node.left
                node.left.parent = None
            elif node == node.parent.left:
                node.parent.left = node.left
                node.left.parent = node.parent
            else:
                node.parent.right = node.left
                node.left.parent = node.parent
        else:
            successor = self._find_leftmost_right(node.right)
            node.content = successor.content
            self.node_map[node.content] = node
            self._delete_node(successor)

        self._update_size_and_height(node.parent)
        self._balance_tree(node.parent)

    def _find_leftmost_right(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _update_size_and_height(self, node):
        while node is not None:
            node.subtree_size = 1 + self._get_size(node.left) + self._get_size(node.right)
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
            node = node.parent

    def _get_size(self, node):
        if node is None:
            return 0
        return node.subtree_size

    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _balance_tree(self, node):
        while node is not None:
            balance = self._get_balance(node)
            if balance > 1:
                if self._get_balance(node.left) < 0:
                    node.left = self._rotate_left(node.left)
                node = self._rotate_right(node)
            elif balance < -1:
                if self._get_balance(node.right) > 0:
                    node.right = self._rotate_right(node.right)
                node = self._rotate_left(node)
            self._update_size_and_height(node)
            node = node.parent

    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        if new_root.left is not None:
            new_root.left.parent = node
        new_root.left = node
        new_root.parent = node.parent
        node.parent = new_root
        if new_root.parent is None:
            self.root = new_root
        elif new_root.parent.left == node:
            new_root.parent.left = new_root
        else:
            new_root.parent.right = new_root
        self._update_size_and_height(node)
        self._update_size_and_height(new_root)
        return new_root

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        if new_root.right is not None:
            new_root.right.parent = node
        new_root.right = node
        new_root.parent = node.parent
        node.parent = new_root
        if new_root.parent is None:
            self.root = new_root
        elif new_root.parent.left == node:
            new_root.parent.left = new_root
        else:
            new_root.parent.right = new_root
        self._update_size_and_height(node)
        self._update_size_and_height(new_root)
        return new_root

    def get_rank(self, content):
        if content not in self.node_map:
            raise ValueError("Content not found in the tree")
        node = self.node_map[content]
        rank = 0
        if node.left is not None:
            rank += self._get_size(node.left)

        while node.parent is not None:
            if node == node.parent.right:
                rank += self._get_size(node.parent) - self._get_size(node)
            node = node.parent
        return rank


def calculate_reuse_distance(traceFile):
    tree = Tree()
    last_occurrence = {}
    reuse_distances = {"avg": 0, "min": float('inf'), "max": -1, "variance": 0, "median": 0, "0": 0}
    list_reuse_distances = []
    index = 1
    while index <= 512 * 1024:
        if index < 1024:
            reuse_distances[str(index)] = 0
        else:
            temp = index / 1024
            reuse_distances[str(temp) + "K"] = 0
        index *= 2
    reuse_distances['>512K'] = 0
    with open(traceFile, 'r') as file:
        rows = file.readlines()
        for i, row in enumerate(rows):
            time_stamp, _, offset, _, _, _, _, _ = row.strip().split(',')
            if offset in last_occurrence:
                last_index = last_occurrence[offset]
                rank = tree.get_rank(last_index)
                list_reuse_distances.append(rank)
                tree.delete(last_index)
            last_occurrence[offset] = i
            tree.insert(i)
    convert_list_to_output(reuse_distances, list_reuse_distances)
    return reuse_distances


def convert_list_to_output(reuse_distances, data_list):
    # reuse_distances['mode'] = most_frequent(data_list)
    data_list = np.array(data_list)
    reuse_distances['variance'] = np.std(data_list) ** 2
    reuse_distances['avg'] = np.mean(data_list)
    reuse_distances['median'] = np.median(data_list)
    for element in data_list:
        update_reuse_distance(element, reuse_distances)

def update_reuse_distance(rank, reuse_distances):
    if rank == 0:
        reuse_distances["0"] += 1
    elif rank == 1:
        reuse_distances["1"] += 1
    elif rank == 2:
        reuse_distances["2"] += 1
    elif rank < 4:
        reuse_distances["4"] += 1
    elif rank < 8:
        reuse_distances["8"] += 1
    elif rank < 16:
        reuse_distances["16"] += 1
    elif rank < 32:
        reuse_distances["32"] += 1
    elif rank < 64:
        reuse_distances["64"] += 1
    elif rank < 128:
        reuse_distances["128"] += 1
    elif rank < 256:
        reuse_distances["256"] += 1
    elif rank < 512:
        reuse_distances["512"] += 1
    elif rank < 1024:
        reuse_distances["1.0K"] += 1
    elif rank < 2048:
        reuse_distances["2.0K"] += 1
    elif rank < 4 * 1024:
        reuse_distances["4.0K"] += 1
    elif rank < 8 * 1024:
        reuse_distances["8.0K"] += 1
    elif rank < 16 * 1024:
        reuse_distances["16.0K"] += 1
    elif rank < 32 * 1024:
        reuse_distances["32.0K"] += 1
    elif rank < 64 * 1024:
        reuse_distances["64.0K"] += 1
    elif rank < 128 * 1024:
        reuse_distances["128.0K"] += 1
    elif rank < 256 * 1024:
        reuse_distances["256.0K"] += 1
    elif rank < 512 * 1024:
        reuse_distances["512.0K"] += 1
    else:
        reuse_distances[">512K"] += 1

    if rank > reuse_distances['max']:
        reuse_distances['max'] = rank
    if rank < reuse_distances['min']:
        reuse_distances['min'] = rank

def add_to_output(traceFile, reuse_distances):
    dataList = [traceFile]
    for key in reuse_distances.keys():
        dataList.append(reuse_distances[key])
    with open('output.csv', 'a', newline='') as outFile:
        writer = csv.writer(outFile)
        writer.writerow(dataList)


cmd = "find . -type f  -name 'A*.csv' | awk -F/ '{print $NF}'"
traceFiles = os.popen(cmd).read().split("\n")
traceFiles.pop()
for traceFile in traceFiles:
    reuse_distances = calculate_reuse_distance(traceFile)
    add_to_output(traceFile, reuse_distances)
