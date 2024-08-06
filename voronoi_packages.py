import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def distance_to_line(self, line):
        if line.get_slope() is None:
            # for vertical lines, calculate the distance to the line based on the x coordinate
            return abs(self.x - line.start.x)
        else:
            # calculate the distance to the line using the formula for the distance between a point and a line
            return abs(line.get_slope() * self.x - self.y + line.get_y_intercept()) / ((line.get_slope() ** 2 + 1) ** 0.5)
    
    def __str__(self):
        return f'{(self.x, self.y)}'
    
    def eq(self, other, interv=0):
        return abs(self.x - other.x) <= interv and abs(self.y - other.y) <= interv
        #return (self.x, self.y) == (other.x, other.y)
    
    def plot(self, color='b', marker='o'):
        plt.plot(self.x, self.y, color=color, marker=marker)
        
class Intersection(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.seg1 = None
        self.seg2 = None
        
    def remove(self):
        self.seg1.remove_intr(self)
        self.seg2.remove_intr(self)

class Line:
    def __init__(self, start, end):
        self.start = start if isinstance(start, Point) else Point(*start)
        self.end = end if isinstance(end, Point) else Point(*end)
        self.intr_list = []
        self.complete = False

    def get_slope(self):
        if self.end.x - self.start.x != 0:
            return (self.end.y - self.start.y) / (self.end.x - self.start.x)
        else:
            return None

    def get_y_intercept(self):
        return self.start.y - (self.get_slope() * self.start.x) if self.get_slope() is not None else self.start.x

    def intersects(self, other):
        # get slopes and y-intercepts of each line
        m1, b1 = self.get_slope(), self.get_y_intercept()
        m2, b2 = other.get_slope(), other.get_y_intercept()

        # check for parallel lines
        if m1 == m2:
            return False

        # check for undefined slopes
        if m1 is None:
            x = self.start.x
            y = (m2 * x) + b2
        elif m2 is None:
            x = other.start.x
            y = (m1 * x) + b1
        else:
            # calculate intersection point
            x = (b2 - b1) / (m1 - m2)
            y = (m1 * x) + b1

        # check if intersection point is within both line segments
        if (self.start.x <= x <= self.end.x or self.start.x >= x >= self.end.x) \
                and (other.start.x <= x <= other.end.x or other.start.x >= x >= other.end.x):
            return Intersection(x, y)

        # otherwise, lines do not intersect
        return False
    
    def same_side(self, p1, p2):
        if self.get_slope() is None:
            # for vertical lines, check if both points have the same x value
            return p1.x == p2.x == self.start.x or (p1.x < self.start.x and p2.x < self.start.x) or (p1.x > self.start.x and p2.x > self.start.x)
        else:
            # calculate the y value of the line for each point and compare their signs
            return (self.get_slope() * p1.x + self.get_y_intercept() - p1.y) * \
                   (self.get_slope() * p2.x + self.get_y_intercept() - p2.y) >= 0
    
    def add_intr(self, intr):
        self.intr_list.append(intr)
        
    def remove_intr(self, intr):
        self.intr_list.remove(intr)
        
    def sort_intr(self, target):
        self.intr_list.sort(key=lambda a : a.distance(target))
        
    def is_complete(self):
        if len(self.intr_list) == 2 and set([(i.x, i.y) for i in self.intr_list]) == set([(i.x, i.y) for i in [self.start, self.end]]):
            return True
        else: return False
        
    def __str__(self):
        return f'Line: [{self.start} {self.end}]'
    
    def __getitem__(self, key):
        if key == 0:
            return self.start
        elif key == 1:
            return self.end
        else:
            raise IndexError("Index must be 0 or 1")
            
    def tup_rep(self):
        return ((self.start.x, self.start.y), (self.end.x, self.end.y))
    
    def __eq__(self, other):
        if other is not None:
            return (self.start.eq(other.start, 0.05) and self.end.eq(other.end, 0.05)) or (self.start.eq(other.end, 0.05) and self.end.eq(other.start, 0.05))

    def plot(self, color='b'):
        plt.plot([self.start.x, self.end.x], [self.start.y, self.end.y], color=color)

if __name__ == '__main__':
    # create some points
    p1 = Point(0, 0)
    p2 = Point(5, 4)
    p3 = Point(5, 0)
    p4 = Point(0, 5)
    
    # create some lines
    l1 = Line(p1, p2)
    l2 = Line(p3, p4)
    
    # check if lines intersect and get intersection point
    intersection = l1.intersects(l2)
    
    if intersection:
        print(f"The lines intersect at ({intersection.x}, {intersection.y})")
    else:
        print("The lines do not intersect")
    
    # plot the lines
    l1.plot()
    l2.plot()
    intersection.plot()
    plt.show()