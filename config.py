class User:
    def __init__(self, d, price_centroid):
        self.d = d
        self.price_centroid = price_centroid
        self.is_responding = False


a = 10
b = 73
c = 1

user1 = User(0, 3)
user2 = User(3, 2.5)
user3 = User(2, 4)
user4 = User(0, 3.5)
user5 = User(4, 2)
user_list = [user1, user2, user3, user4, user5]

coefficients = [0, 3, 2, 0, 4]
centroids = [3, 2.5, 4, 3.5, 2]
loadData = [300,308,315,320,325,329,333,336,340,344,349,354,356,360,367,370,372,375,
            379,382,385,387,389,391,394,396,397,398,396,393,389,386,382,380,376,
            370,363,356,352,349,350,351,354,358,361,366,370,374,376,380,383,387,
            390,394,399,406,414,423,435,450,466,481,496,511,526,542,560,578,598,
            616,636,640,643,642,638,630,612,592,572,550,532,510,488,462,438,416,
            392,370,345,335,323,314,310,308,307,306]

#user_list = [User(d, centroid) for d,centroid in zip(coefficients, centroids)]
