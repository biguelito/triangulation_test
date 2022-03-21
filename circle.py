import math

class Circle(object):
    """ An OOP implementation of a circle as an object """

    def __init__(self, xposition, yposition, radius):
        self.xpos = xposition
        self.ypos = yposition
        self.radius = radius
        self.precision = 5

    def circle_intersect(self, circle2):
        X1, Y1 = self.xpos, self.ypos
        X2, Y2 = circle2.xpos, circle2.ypos
        R1, R2 = self.radius, circle2.radius

        Dx = X2-X1
        Dy = Y2-Y1
        D = round(math.sqrt(Dx**2 + Dy**2), self.precision)
        if D > R1 + R2:
            return (0, 0, "The circles do not intersect")
        elif D < math.fabs(R2 - R1):
            return (0, 0, "No Intersect - One circle is contained within the other")
        elif D == 0 and R1 == R2:
            return (0, 0, "No Intersect - The circles are equal and coincident")
        else:
            if D == R1 + R2 or D == R1 - R2:
                CASE = "The circles intersect at a single point"
            else:
                CASE = "The circles intersect at two points"
            chorddistance = (R1**2 - R2**2 + D**2)/(2*D)
            halfchordlength = math.sqrt(R1**2 - chorddistance**2)
            chordmidpointx = X1 + (chorddistance*Dx)/D
            chordmidpointy = Y1 + (chorddistance*Dy)/D
            I1 = (round(chordmidpointx + (halfchordlength*Dy)/D, self.precision),
                  round(chordmidpointy - (halfchordlength*Dx)/D, self.precision))
            theta1 = round(math.degrees(math.atan2(I1[1]-Y1, I1[0]-X1)),
                           self.precision)
            I2 = (round(chordmidpointx - (halfchordlength*Dy)/D, self.precision),
                  round(chordmidpointy + (halfchordlength*Dx)/D, self.precision))
            theta2 = round(math.degrees(math.atan2(I2[1]-Y1, I2[0]-X1)),
                           self.precision)
            if theta2 > theta1:
                I1, I2 = I2, I1
            return (I1, I2, CASE)