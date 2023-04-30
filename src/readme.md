# simple use of simple mail transport protocol library.

# protocol abstracts networking principles away from smtp client and server, so that session can be opened between them.

# send email after set time as long as the program is running.

# process runs once per day with logic checking if the dates are different.

# quotes which make up email contents are scrapped from url in accompanying script.

# quotes are randomly selected for in list object and returned to give emails varying content.

# script is automated as a background process by cronjobs, allowing for scheduled tasks to be executed.

# process title logic is to ensure only one instance of the process is running at a time, this is make the program more efficient when considering CPU and memory.
