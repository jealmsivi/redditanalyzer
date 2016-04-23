# redditanalyzer

If you've posted on Reddit long enough then you'll probably know it's a pain to find old posts of yours. The system is locked in at 1000 comments, at least when viewed by "new". You can see older posts by messing around with the sort options -- "top", "controversial", etc. but it's a real pain. This is a program that sets out to fix that problem, as far as one can use a command line based desktop program to fix a website.

# Requirements
You're going to need Python, version 3 or above to run it. It's also Windows only, although I suspect a Linux version wouldn't be very hard to create (a few minor changes).

# How to use
Simply run the script, and follow along with the prompts. First off you will have to archive a new user's posts to do anything useful. This process might take a few minutes. Essentially the program is scraping all the comments it can find for the user. This is not a perfect process and it doesn't get every post ever but I've had luck getting truly old ones. For long time users I've seen an upwards of 3000+ posts found.

Once done the program will have created a text file with all the posts in the script's directory. As of the current version these text files must remain in the script's directory to be recognized and work. It will be named after the user with the extension ".raf". This file will be used by the analyzer in the next step but also serves as a sort of archive. Reddit won't be around forever so why not have your posts or the posts of others in a nicely formatted text file?

Now it's time to analyze a user. Enter the username you want to analzye. Please note that you need that username's .raf file before you can do anything! Once you enter the username you will see a quick summary of all the posts found: total comment karma (a simple sum of all comment karma found), # of posts and # of subreddits posted in. You can type in v and then a sorting option (alphabetical, by most karma, by most posts) to see a list of all the subreddits that were posted in by the user. This list will be of great use when trying to find specific posts!

Next type in a subreddit name. This will allow you to see all the posts in that subreddit, sorted by top karma, newest, or oldest. Note that you can type "all" in to the prompt when asked to type in a subreddit name to see all the posts that the program found for the user. You can also type in s to search for a specific word or phrase in all the posts for that subreddit. This can be very useful when you're examining all the posts of the user.

# Long term use
Once the posts of a user are archived it would be a pain to have to re-archive them all again when new posts are made. Luckily if you return to the archive screen and type in a username that is already archived it will update -- only new posts that haven't been archived will be added to the .raf file. This, of course, does not have to be done and is simply there as a quality of life feature.
