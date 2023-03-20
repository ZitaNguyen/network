# Network
Design a Twitter-like social network website for making posts and following users by using Python, Javascript, HTML, and CSS.

## Functionalities

### All Posts
* A page shows all posts from all users, with the most recent posts first.
* Each post includes the username of the poster, the post content, the date and time at which the post was made, and the number of “likes” the post has.

### New Post
* Users who are signed in can write a new text-based post by filling in text into a textarea and then clicking a button to submit the post.

### Edit Post
* When a user clicks “Edit” for one of their own posts, the content of their post is replaced with a textarea where teh user can edit the content of their post.
* The user can “Save” the edited post. By using Javascript, the application can achieve this without requiring a reload of the entire page.
* A user cannot edit another user’s posts.

### Profile Page
* Clicking on a username will load that user’s profile page. 
* This page display the number of followers the user has, as well as the number of people that the user follows.
* This page display all of the posts for that user, in reverse chronological order.
* For any other user who is signed in, this page displays a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts.
* Note: a user cannot follow themselves.

### Following
* A page displays all posts made by users that the current user follows.
* This page behaves just as “All Posts” page, and is only available to users who are signed in.

### Pagination
* On any page that displays posts, posts should only be displayed 10 on a page.
* If there are more than 10 posts, a “Next” button appears to take the user to the next page of posts (which is older than the current page of posts)
* If not on the first page, a “Previous” button appears to take the user to the previous page of posts as well.

### "Like" and "Unlike"
* Users can click a button to toggle whether or not they “like” that post.
* Using Javascript, the application can asynchronously let the server know to update the like count, and then update the post’s like count displayed on the page, without requiring a reload of the entire page.
