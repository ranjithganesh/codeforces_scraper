import time
import getpass
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_tab():
    
    tab = webdriver.Firefox()
    tab.wait = WebDriverWait(tab, 2)
    return tab

def get_problem_link():

	return raw_input("Enter url of the problem you want to verify: ")

def enter(tab):
	
	tab.get("http://codeforces.com/")
	tab.implicitly_wait(2) 

	enter = tab.find_element_by_link_text('Enter')
	enter.click()
	tab.implicitly_wait(2) 

	handle = tab.wait.until(EC.presence_of_element_located((By.ID, "handle")))
	# handle.send_keys(raw_input("Enter Handle: "))
	handle.send_keys("TooDifferent")

	password = tab.wait.until(EC.presence_of_element_located((By.ID, "password")))
	password.send_keys(getpass.getpass("Enter Password: "))

	submit = tab.find_element_by_xpath("/html/body/div[2]/div[4]/div/div/div/form/table/tbody/tr[4]/td/div[1]/input")
	submit.click()

def find_tags(tab):
	
	dict = {}

	pages = "http://codeforces.com/problemset/page/"
	for x in xrange(1, 36):
		
		tab.get(pages + str(x))
		tab.implicitly_wait(2)

		link = "/html/body/div[2]/div[4]/div[2]/div[2]/div[6]/table/tbody"
		
		total_problems = len(tab.find_element_by_xpath(link).find_elements_by_css_selector("tr"))

		for i in xrange(2,total_problems + 1):
			
			problem = link + "/tr[" + str(i) + "]/"
			
			# name = problem + "td[1]/a"
			# print tab.find_element_by_xpath(name).text

			tags = problem + "td[2]/div[2]"
			list_tags = tab.find_element_by_xpath(tags).find_elements_by_css_selector("a")
			
			for tag in list_tags:
				if tag.text.encode('ascii','ignore') not in dict.keys():
					dict[tag.text.encode('ascii','ignore')] = 1
				else:
					dict[tag.text.encode('ascii','ignore')] += 1	

	tab.quit()

	fout = open("probems_in_tags.txt", 'w')
	fout2 = open("tags_list.txt", 'w')

	for k,v in dict.items():
   		fout.write(str(k).ljust(27) + str(v) + '\n')
   		fout2.write(str(k) + '\n')
	fout.close()
	fout2.close()	

	tab.quit()

def solved_problem(tab, user, problem_link):

	submissions_link = "http://codeforces.com/submissions/"
	user_link = submissions_link + user
	pages_link = user_link + "/page/"
	
	try:
		tab.get(user_link)
		if tab.current_url != user_link:
			raise
	except:		
		print "No such handle found ..."
		tab.quit() 
		return 

	try:
		xpath = "/html/body/div[2]/div[4]/div[2]/div[9]/ul"
		num_pages = len(tab.find_element_by_xpath(xpath).find_elements_by_css_selector("li"))
		tab.implicitly_wait(2)
		
		last_page = xpath + "/li[" + str(num_pages - 1) + "]/span"
		number_pages = int(tab.find_element_by_xpath(last_page).find_element_by_css_selector("a").text)
		tab.implicitly_wait(2)
		
	except:
		print "User has only 1 page ..."
		number_pages = 1

	flag = False

	for i in xrange(1, number_pages + 1):

		tab.get(pages_link + str(i))

		submit_path = "/html/body/div[2]/div[4]/div[2]/div[4]/div[6]/table/tbody"
		number_submit = len(tab.find_element_by_xpath(submit_path).find_elements_by_css_selector("tr"))	
		
		for j in xrange(2, number_submit + 1):

			submission_row_link = submit_path + "/tr[" + str(j) + "]/td[4]"
			accepted_row_link = submit_path + "/tr[" + str(j) + "]/td[6]"
			solution_row_link = submit_path + "/tr[" + str(j) + "]/td[1]"

			verify_link = tab.find_element_by_xpath(submission_row_link).find_element_by_css_selector("a").get_attribute("href")
			result = tab.find_element_by_xpath(accepted_row_link).find_element_by_css_selector("span").get_attribute("submissionverdict")

			if result == "OK" and problem_link == verify_link:
				
				print tab.find_element_by_xpath(solution_row_link).find_element_by_css_selector("a").get_attribute("href")
				flag = True

		if flag:
			return True

	print "User hasn't got the problem accepted ..."
	return False

	tab.quit()

def task_for_team(tab, team):

	problem_link = get_problem_link()	

	for member in team:

		if solved_problem(tab, member, problem_link) == True:
			print member.upper() + " has already solved the problem ..."
			break

	else:		
		print "The problem can be used in the contest"

	tab.quit()
	
def blogs(tab):

	common_link = "http://codeforces.com/blog/entry/"

	fout = open("blog_details.txt", 'w')
	fout2 = open("good_blog_links", 'w')
	fout3 = open("good_tutorial_links", 'w')

	for i in xrange(1, 1000):
		
		tab.get(common_link + str(i))
		tab.implicitly_wait(1) 

		url_current = tab.current_url
	
		try:	

			if url_current != common_link + str(i):
				alert
			

			headline_xpath = "/html/body/div[2]/div[4]/div[2]/div[2]/div[2]/div/div[2]"
 			language = tab.find_element_by_xpath(headline_xpath).find_element_by_css_selector("img").get_attribute('title')
					
 			if language == "In Russian":
 				message = " The blog requested is in Russian ..."

 			else:  
 				
 				span_list = tab.find_elements_by_css_selector("span[title]")
 				upvotes = 0

 				for span in span_list:
 					
 					if span.get_attribute("title") == "Topic rating":
 						upvotes = int(span.text)
 						break

 				if upvotes > 15:
 					message = " The number of upvotes is: " + str(upvotes)
 					fout2.write(url_current + '\n')
 					print url_current

 					title_xpath = "/html/body/div[2]/div[4]/div[2]/div[2]/div[2]/div/div[1]/a"
 					to_check_existance_of_p = tab.find_element_by_xpath(title_xpath).find_elements_by_css_selector("p")
 					
 					if to_check_existance_of_p == []:
						heading = tab.find_element_by_xpath(title_xpath).text 						

					else:
						heading = tab.find_element_by_xpath(title_xpath).find_element_by_css_selector("p").text	
 					
 					if heading[-10:] == "[Tutorial]":
 						fout3.write(url_current + '\n')
 						print "Tutorial ..."

 				else:
 					message = " The blog is not worth seeing as it has very low upvotes ..."

 		except:

 			message = " The blog requested does not exist / not accessible ..."			
		
		fout.write(str(i) + message + '\n') 
	
	fout.close()
	fout2.close()
	fout3.close()

	tab.quit()
	
if __name__ == "__main__":

	tab = init_tab()
    
	# tab = enter(tab) # To login into http://codeforces.com/
    
	# find_tags(tab) # To find the number of problems throughout in each tag 

	# user = raw_input("Enter the handle to search: ")
	# solved_problem(tab, user, get_problem_link())
	
	blogs(tab)

	# team = ["ralekseenkov", "megabidoof", "MikeMirzayanov"]
	# task_for_team(tab, team)