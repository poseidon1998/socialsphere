from django.db import models # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from django.core.validators import MinLengthValidator,MaxLengthValidator # type: ignore
from . import choices # type: ignore

class SS_User(models.Model):
    user_name = models.CharField(max_length=225,db_column="user_name",blank=False,null=False)
    category = models.IntegerField(db_column="category",blank=False,null=False,choices=choices.get_choices('SS_User', 'category'))         
    active_status = models.BooleanField(db_column='active_status',default=True)
    login_time = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=255, db_column="email", blank=False, null=False,unique=True)
    password = models.CharField(
    max_length=128, 
    db_column="password", 
    blank=False, 
    null=False, 
    validators=[MinLengthValidator(8), MaxLengthValidator(20)]
)

    class Meta:
        db_table = 'SS_User'
        verbose_name_plural = 'SS_User'

    def __str__(self):
        return str(self.user_name)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        if not any(char.isdigit() for char in self.password) or not any(char.isalpha() for char in self.password):
            raise ValidationError("Password must contain at least one letter and one number.")
        super().save(*args, **kwargs)
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(SS_User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(SS_User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='request sent', choices=choices.get_choices('FriendRequest', 'status'))

    class Meta:
        db_table = 'FriendRequest'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"Request from {self.from_user} to {self.to_user} - {self.status}"

    def accept(self):
        # Update the status to accepted
        self.status = 'accepted'
        self.save()
        
        # Add both users to each other's friends list
        from_user_friends_list, created = FriendsList.objects.get_or_create(user=self.from_user)
        to_user_friends_list, created = FriendsList.objects.get_or_create(user=self.to_user)

        from_user_friends_list.friends.add(self.to_user)
        to_user_friends_list.friends.add(self.from_user)

class FriendsList(models.Model):
    user = models.OneToOneField(SS_User, related_name='friends_list', on_delete=models.CASCADE)
    friends = models.ManyToManyField(SS_User, related_name='friend_of')  # Corrected this line

    class Meta:
        db_table = 'FriendsList'

    def __str__(self):
        return f"{self.user.user_name}'s friends list"

