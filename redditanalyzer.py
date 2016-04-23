import praw, json, subprocess, time, os, re

def main():

	intro()
	
	while True:
		
		print("Do you want to archive a (n)ew user, analyze an (e)xisting user, or (q)uit?")
		
		userInput = input("> ").lower()
		
		if userInput == "q":
			
			clearScreen()
			break
		
		elif userInput == "n":
			
			while True:
			
				clearScreen()
				print("Archiving a new user's posts.")
				print("Please input a user name or (q)uit to go back one screen.")
				
				username = input("> ").lower()
				
				if username == "q":
					clearScreen()
					break
					
				elif len(username) >= 3: #a valid reddit username must be at least three characters. this acts as a sort of simple error checking
					
					usernameList = getAndReturnUsernameList()
					
					if username in usernameList:
						
						print()
						print("Updating posts. This might take a while...")
						
						archiveComments(username, [u'new'], "a")
						
						print()
						print("Posts updated! Feel free to use the analyzer to examine the posts.")
						
					else:
					
						print()
						print("Archiving posts. This might take a while...")
					
						archiveComments(username, [u'top', u'new', u'hot', u'controversial'], "w")
					
						print()
						print("Posts archived! Feel free to use the analyzer to examine the posts.")
						
					print()
					input("Hit enter to continue.")
					
					clearScreen()
					
					break
					
				else:
				
					badInputResponse()
					clearScreen()
			
		elif userInput == "e":
		
			while True:
			
				clearScreen()
				
				print("Analyzing an existing user.")
				
				print()
				
				print("Please input a user name, (v)iew the list of usernames ready to analyze, or (q)uit to go back one screen.")
				
				username = input("> ").lower() #I don't think it matters if usernames are lowercase or not. Easier to work with
				
				usernameList = getAndReturnUsernameList()
				usernameList.sort()
				
				print()
				
				if username == "q":
					clearScreen()
					break
					
				elif username == "v":
					clearScreen()
					
					print("List of usernames (alphabetical): ")
					
					print()
					
					for username in usernameList:
						print(username)
						
					print()
					
					input("Hit enter to continue.")
					
				elif len(username) >= 3 and username in usernameList:
					clearScreen()
					
					subredditDictionary = buildSubredditDictionary(username)
					
					while True:
					
						print("Quick summary: ")
						
						print()
					
						print("{0} posts in {1} subreddits.".format(len(subredditDictionary["all"]["posts"]), len(subredditDictionary.keys()) - 1))
						print("{0} total karma.".format(subredditDictionary["all"]["karma"]))
					
						print()
					
						print("Analyzing " + username + ".")
						print("Please type a subreddit name to see the posts from that subreddit.")
						print("You can also (v)iew the list of subreddits (with # of posts and karma) or (q)uit to the previous screen.")
					
						mainUserInput = input("> ").lower()
						
						if mainUserInput == "q":
							clearScreen()
							break
							
						elif mainUserInput == "v":
									
							clearScreen()
							
							while True:
							
								print("Viewing list of subreddits.")
								print("Sort list by (a)lphabetical, (k)arma, or (p)osts?")
								print("(Q)uit to return to the previous screen.")
								
								viewUserInput = input("> ").lower()
								
								clearScreen()
								
								if viewUserInput == "q":
									clearScreen()
									break
									
								elif viewUserInput in ["a", "k", "p"]:
									
									listOfSubInfo = []
									
									for sub in list(subredditDictionary.keys()):
										#subreddit name, subreddit karma, subreddit # of posts
										listOfSubInfo.append([sub, subredditDictionary[sub]["karma"], len(subredditDictionary[sub]["posts"])])
															
									if viewUserInput == "a": #alphabetical
									
										print("List of subreddits (alphabetical): ")
										print()
										sortedListOfSubInfo = sorted(listOfSubInfo, key=lambda alpha: alpha[0])
											
									elif viewUserInput == "k": #karma
											
										print("List of subreddits (karma): ")
										print()
										sortedListOfSubInfo = sorted(listOfSubInfo, key=lambda karma: karma[1], reverse=True)
										
									elif viewUserInput == "p": #posts
									
										print("List of subreddits (posts): ")
										print()
										sortedListOfSubInfo = sorted(listOfSubInfo, key=lambda posts: posts[2], reverse=True)
										
										
									for infoArray in sortedListOfSubInfo:
										
										sub = infoArray[0]
											
										print("{0:<30}{1:>15}{2:>15}".format(sub, "(" + str(len(subredditDictionary[sub]["posts"])) + " posts)", "(" + str(subredditDictionary[sub]["karma"]) + " karma)"))
										print()
										
								else:
								
									badInputResponse()
									
									clearScreen()
									
								
						elif len(mainUserInput) >= 3 and mainUserInput in list(subredditDictionary.keys()):
						
							clearScreen()
						
							while True:
														
								print("Viewing posts in " + mainUserInput + ".")
								print("Sort by (t)op, (n)ewest, or (o)ldest?")
								print("(S)earch posts for words and phrases.")
								print("(Q)uit to return to the previous screen.")
								
								subUserInput = input("> ").lower()
								
								if subUserInput == "q":
									clearScreen()
									break
									
								elif subUserInput in ["t", "n", "o"]:
																	
									clearScreen()						
																	
									sortPosts(subUserInput, subredditDictionary, mainUserInput)
									
								elif subUserInput == "s":
								
									clearScreen()
									
									print("Enter a string to search for.")
									searchTerm = input("> ")
									
									searchPosts(mainUserInput, subredditDictionary, searchTerm) #the subreddit, the info on the poster and the keywords/phrases
									
								else:
								
									badInputResponse()
									
									clearScreen()
									
						else:
						
							badInputResponse()
							
							clearScreen()
				
				else:
				
					badInputResponse()
					
					clearScreen()
				
		else:
		
			badInputResponse()
			
			clearScreen()
			
def searchPosts(subreddit, subredditDictionary, searchTerm):
	
	clearScreen()
	
	print("Searching {0} posts in {1} for '{2}'.".format(len(subredditDictionary[subreddit]["posts"]), subreddit, searchTerm))
	
	listOfPosts = []
	
	for post in subredditDictionary[subreddit]["posts"]:
	
		if re.search(searchTerm.lower(), post["body"].lower()):
		
			listOfPosts.append(post)
			
	if len(listOfPosts) > 0:
	
		printSortedPosts(listOfPosts)
		
	else:
	
		print()
		input("Nothing found! Press enter to continue.")
		
		clearScreen()
			
def archiveComments(username, listOfSortTypes, openFileMode):
	
	if openFileMode == "w":
	
		listOfPostId = []
		
	else:
		
		usernameFileIdBuilder = open(username + ".raf", "r", encoding='utf-8') 
		
		listOfPostId = []
		
		for line in usernameFileIdBuilder.readlines():
		
			jsonLine = json.loads(line)
		
			uniqueId = jsonLine["link_id"] + jsonLine["id"]
			listOfPostId.append(uniqueId)
			
		usernameFileIdBuilder.close()
		
		
	usernameFile = open(username + ".raf", openFileMode, encoding='utf-8')

	r = praw.Reddit(user_agent = "Reddit Archiver/Analyzer")
	me = r.get_redditor(username)
					
	for sortType in listOfSortTypes:
					
		for x in me.get_comments(limit = None, sort = sortType):
						
			uniquePostId = x.__dict__["link_id"] + x.__dict__["id"]
						
			if uniquePostId not in listOfPostId:
							
				listOfPostId.append(uniquePostId)
							
				newDict = {}
								
				oldDict = x.__dict__
								
				newDict["body"] = oldDict["body"]
				newDict["created"] = oldDict["created"]
				newDict["created_utc"] = oldDict["created_utc"]
				newDict["link_title"] = oldDict["link_title"]
				newDict["score"] = oldDict["score"]
				newDict["subreddit"] = str(oldDict["subreddit"]).lower() #lower case makes it easier for user to input in analyzer
				newDict["link_id"] = oldDict["link_id"]
				newDict["id"] = oldDict["id"]
								
				usernameFile.write(json.dumps(newDict) + "\n")
				
			else:
			
				#this should just get the newest comments, the ones that are already not archived
				#if the program gets to a post that is already in the archive then break out of the for loops. should end archiving process
			
				if len(listOfSortTypes) == 1 and u"new" in listOfSortTypes:
				
					break
			
	usernameFile.close()
									
def getAndReturnUsernameList():

	#the username files are going to have the .raf extension and should be in the same directory as the redditAnalyze script
	
	scriptDirectory = os.listdir()
	
	userNameList = []
	
	for file in scriptDirectory:
		if ".raf" in file:
			userNameList.append(file.split(".raf")[0].lower()) #gets the filename without the extension, user doesn't need to see extension or include it when typing in the program
			
	return userNameList
								
def sortPosts(sortMethod, subredditDictionary, subreddit):

	print()
	print("Examining {0} posts in {1}.".format(len(subredditDictionary[subreddit]["posts"]), subreddit))

	if sortMethod == "t": #highest karma
	
		print("Sorting by top (highest karma at top).")
		sortedPosts = sorted(subredditDictionary[subreddit]["posts"], key=lambda postscore: postscore["score"], reverse=True)
		
	elif sortMethod == "n": #newest
	
		print("Sorting by newest (newest at top).")
		sortedPosts = sorted(subredditDictionary[subreddit]["posts"], key=lambda posttime: posttime["created_utc"], reverse=True)
		
	elif sortMethod == "o": #oldest
	
		print("Sorting by oldest (oldest at top).")
		sortedPosts = sorted(subredditDictionary[subreddit]["posts"], key=lambda posttime: posttime["created_utc"])

	print()
	
	printSortedPosts(sortedPosts)

def printSortedPosts(sortedPosts):

	viewString = ""
	
	for post in sortedPosts:
		'''
		print("\n##################################################\n")
		
		print("THREAD TITLE: \n")
		print(post["link_title"].encode("ascii", "replace"))
				
		print()
		
		print("THREAD LINK: https://redd.it/" + post["link_id"].split("_")[1] + "\n")
		
		print()
		
		print("COMMENT SCORE: " + str(post["score"]))
		
		print()
		
		print("DAY AND TIME: " + time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(post["created_utc"])))
		
		print()
		
		print("COMMENT: \n")
		print(post["body"].encode("ascii", "replace"))
		
		print("\n##################################################\n")
		'''
		
		viewString += "\n##################################################\n"
		viewString += "THREAD TITLE: "
		viewString += post["link_title"].encode("ascii", "replace").decode()
		viewString += "\n\n"
		viewString += "THREAD LINK: https://redd.it/" + post["link_id"].split("_")[1]
		viewString += "\n\n"
		viewString += "COMMENT SCORE: " + str(post["score"])
		viewString += "\n\n"
		viewString += "DAY AND TIME: " + time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(post["created_utc"]))
		viewString += "\n\n"
		viewString += "COMMENT: "
		viewString += "\n\n"
		viewString += post["body"].encode("ascii", "replace").decode()
		viewString += "\n##################################################\n"
		
	print(viewString)
					
def intro():

	clearScreen()

	print("REDDIT ARCHIVER/ANALYZER")
	input("Hit enter to continue.")
	
	clearScreen()
	
def badInputResponse():

	input("Please enter a valid input! Hit enter to continue.")
	
def clearScreen():

	subprocess.call("cls", shell = True)
	
def buildSubredditDictionary(username):

	openedFile = open(username + ".raf", "r", encoding='utf-8')

	allLines = openedFile.readlines()

	subredditDictionary = {}

	subredditDictionary["all"] = {}
	subredditDictionary["all"]["posts"] = []
	subredditDictionary["all"]["karma"] = 0

	for line in allLines:

		b = json.loads(line)
			
		subredditDictionary["all"]["posts"].append(b)
		subredditDictionary["all"]["karma"] += int(b["score"])
		
		if b["subreddit"] in subredditDictionary.keys():
			subredditDictionary[b["subreddit"]]["posts"].append(b)
			subredditDictionary[b["subreddit"]]["karma"] += int(b["score"])
			
		else:
			subredditDictionary[b["subreddit"]] = {}
			subredditDictionary[b["subreddit"]]["posts"] = []
			subredditDictionary[b["subreddit"]]["karma"] = 0
			
			subredditDictionary[b["subreddit"]]["posts"].append(b)
			subredditDictionary[b["subreddit"]]["karma"] += int(b["score"])
			
			
	openedFile.close()
	
	return subredditDictionary
	
main()