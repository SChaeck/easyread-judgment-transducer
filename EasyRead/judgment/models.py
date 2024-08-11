from django.db import models

class User(models.Model):
    user_id = models.IntegerField(unique=True)  # 사용자 ID, 고유해야 함

    def __str__(self):
        return f'User {self.user_id}'

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User 모델과의 관계
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])  # 1~5 점수

    def __str__(self):
        return f'Rating for {self.user} - Rating: {self.rating}'

class LowPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User 모델과의 관계
    comment = models.TextField(max_length=700)  # 700자 단위 데이터

    def __str__(self):
        return f'Comment for {self.user} - Comment: {self.comment}'