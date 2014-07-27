#! /usr/bin/env python
#coding:utf8
class Node(object):

    '''''data object in dancing link
    Basic element for a sparse matrix
    doubly linked in both horizontal and vertical direction'''

    def __init__( self, left = None, right = None, up = None, down = None,
            column_header = None, row_header = None ):
        self.left = left or self
        self.right = right or self
        self.up = up or self
        self.down = down or self

        self.column_header = column_header
        self.row_header = row_header

    def nodes_in_direction( self, dir ):
        '''''Generator for nodes in different direction

        :Parameters:
            dir: str
                dir can be 'up', 'down', 'left', 'right'
        '''
        node = getattr( self, dir )
        while node != self:
            #print node.column_header.size
            yield node
            node = getattr( node, dir )

class ColumnHeader(Node):
    '''''list header, or column object in dancing link
    has an extra element of size recording the number of data object in this column'''
    def __init__( self, *args, **kargs ):
        Node.__init__( self, *args, **kargs )
        self.size = 0

class RowHeader(Node):
    '''''RowHeader is an extra element for dancing link to record the row no. of a row
    so that we can trace down which rows are picked up'''

    def __init__( self, rowno, *args, **kargs ):
        Node.__init__( self, *args, **kargs )
        self.rowno = rowno
        self.row_header = self

class DLXSolver(object):

    def __init__( self ):
        pass

    def solve(self, matrix, num_columns):
        '''''solve the exact cover problem of a given matrix

        :Parameters:
            matrix is in the form as:
                { k:[x0, x1, ..., xn] }
            where k is the line number while xi(0<=xi<num_columns) is the column
            of the matrix where there is a 1

            num_columns:
                number of columns in the matrix

        :Return:
            solution: [k]
            solution is a list of line number that is picked
        '''
        self._partial_answer = {}
        self._k = 0
        self._construct( matrix, num_columns )
        self._search(0)

        return [self._partial_answer[k] for k in xrange(self._k)]

    def _construct( self, matrix, num_columns ):
        '''''construct a matrix into a sparse matrix using doubly link list

        :Parameter:
            parameters are same as solve
        '''

        self.root = Node()
        self.column_headers = []

        #constructing column_headers
        for i in xrange(num_columns):
            new_column_header = ColumnHeader(left=self.root.left,
                    right=self.root)
            self.root.left.right = new_column_header
            self.root.left = new_column_header
            self.column_headers.append( new_column_header )



        #inserting nodes into the sparse matrix
        for k in matrix:
            if not matrix[k]:
                continue

            column_id_sorted = sorted(matrix[k])
            column_header = self.column_headers[column_id_sorted[0]]
            column_header.size += 1

            new_row_header = RowHeader(k, up=column_header.up, down=column_header,
                    column_header=column_header)
            column_header.up.down = new_row_header
            column_header.up = new_row_header

            column_id_sorted.pop(0)

            #constructing remaining nodes
            for i in column_id_sorted:
                column_header = self.column_headers[i]
                column_header.size += 1
                new_node = Node( left=new_row_header.left, right=new_row_header,
                        up = column_header.up, down = column_header,
                        column_header = column_header, row_header = new_row_header )
                column_header.up.down = new_node
                column_header.up = new_node
                new_row_header.left.right = new_node
                new_row_header.left = new_node

    def _cover( self, column_header ):
        '''''cover a column of a matrix as what donald said'''

        column_header.left.right = column_header.right
        column_header.right.left = column_header.left

        for eachNode in column_header.nodes_in_direction("down"):
            for node in eachNode.nodes_in_direction("right"):
                node.column_header.size -= 1
                node.up.down = node.down
                node.down.up = node.up

    def _uncover( self, column_header ):
        '''''uncover a column of a matrix in the reverse order as cover do'''

        for eachNode in column_header.nodes_in_direction("up"):
            for node in eachNode.nodes_in_direction("left"):
                node.column_header.size += 1
                node.down.up = node
                node.up.down = node

        column_header.left.right = column_header
        column_header.right.left = column_header

    def _search( self, k ):
        if self.root.right == self.root:
            self._k = k
            return True


        column_header=min([header for header in self.root.nodes_in_direction("right")],
                key=lambda h:h.size)

        self._cover( column_header )
        for eachNode in column_header.nodes_in_direction("down"):
            self._partial_answer[k] = eachNode.row_header.rowno

            for node in eachNode.nodes_in_direction("right"):
                self._cover(node.column_header)

            if self._search( k+1 ):
                return True

            for node in eachNode.nodes_in_direction("left"):
                self._uncover(node.column_header)

        self._uncover(column_header)
        return False

'''''test case for dlxSolver'''
if __name__ == "__main__":
    matrix = { 1:[2, 4,5],
            2:[0,3,6],
            3:[1,2,5],
            4:[0,3],
            5:[1,6],
            6:[3,4,6]}
    testSolver = DLXSolver()
    print testSolver.solve( matrix, 7 )
