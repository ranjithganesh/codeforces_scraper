# codeforces_scraper

This project tries to scrape through http://codeforces.com/ (Codeforces: A competitive
programming website) to obtain useful information. 

	The functions present in the project are: 

		init_tab():

			Initialises the tab(driver). 

		get_problem_link():
		
			Pings user for the the problem link. 

		enter(tab):
			
			For logging into the website, pings for your password in the terminal.	

		find_tags(tab):

			Searches through all the problems in the website, forms a file for the tags which 
			are available and another keeping a count of number of problems in each.

			I'm planning to extend it by providing the problem links (from a particular range of 
			difficulty) of a particular tag.

		solved_problem(tab, user, problem_link):

			The problem link you want to search for and the user who's solution you're 
			considering to look are passed as parameters.

			The function looks through all the submission pages of the user and provides you 
			with the url of the accepted solution if he has done it. 

		task_for_team(tab, team):
			
			Form a team of the users for whom you want to set a problem in a contest 
			(Particularly made for my icpc team and could be extended for the programming club 
			group)

			This basically calls solved_problem as a subroutine and finds if the user has solved 
			the problem already. If no one in the team has solved the problem then the contest 
			could be used in the contest.

			Note: The method I have used here is ineffective if there are a lot of people in the 
			team. I'm planning to fine tune the method ofr teams with more than 5 members.

		blogs(tab):
		
			The blogs in codeforces are not organised properly. In an attempt to the categorise 
			the blogs and to obtain links of all good blogs I have created this function.

			It goes through all the blogs ordered by the index, it handles the non existance of 
			certain links and also eliminates all russian blogs and low quality blogs from 
			consideration.

			It also finds tutorial blogs from the heading and saves them in a seperate file.
			There are two other files having the details of every url being searched and the 
			other having the links of all good blogs.      
	
	I have also added the probems_in_tags.txt and tags_list.txt files after executing the particular function.
	I'm also going to add other interesting features to this project ... So stay tuned !!!
	
