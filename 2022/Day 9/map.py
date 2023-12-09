from numpy import array

TRAILING_MOVE = {
    array([0, 0]): array([0, 0]),

   array([1, 0]): array([0, 0]),
   array([2, 0]): array([1, 0]),
   array([-1, 0]): array([0, 0]),
   array([-2, 0]): array([-1, 0]),

   array([0, 1]): array([0, 0]),
   array([0, 2]): array([0, 1]),
   array([0, -1]): array([0, 0]),
   array([0, -2]): array([0, -1]),

   array([1, 1]): array([0, 0]),
   array([-1, 1]): array([0, 0]),
   array([1, -1]): array([0, 0]),
   array([-1, -1]): array([0, 0]),

   array([2, 1]): array([1, 1]),
   array([-2, 1]): array([-1, 1]),
   array([2, -1]): array([1, -1]),
   array([-2, -1]): array([-1, -1]),

   array([1, 2]): array([1, 1]),
   array([-1, 2]): array([-1, 1]),
   array([1, -2]): array([1, -1]),
   array([-1, -2]): array([-1, -1]),

   array([2, 2]): array([1, 1]),
   array([-2, 2]): array([-1, 1]),
   array([2, -2]): array([1, -1]),
   array([-2, -2]): array([-1, -1])
}
