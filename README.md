# Repeater

A terminal-based application that leverages `browser-use` to automate repetitive web-based tasks.

## How It Works

1. Interact with AI to navigate to a website.
2. Continue the conversation until your objective is achieved.
3. Once finished, the application saves the entire session.
4. You can replay the saved session later.

## Use Case

This can be especially useful for QA purposes, as replaying a session is similar to running regression tests.

> Note: This is an experimental project and not intended for production use.


## How to run

1. Install deps (prefer using uv. Run `uv sync`)
2. Use the virtualenv
3. Run `python main.py` or `make run`
4. Follow the instructions.

## Sample run
```
python main.py

                
 👤 Commands available:
                
 START -> To create a new session
                
 RE -> To replay previous session
                
 ID -> To replay previous session by ID stored
                
 QUERY -> Show all stored data
                
 DEL -> To delete stored session by ID
                
 Your command: start

 👤 Enter name of session: test_open_google_news

 👤 Enter Initial task (e.g. Open google.com): Open news.google.com
INFO     [Agent] 🔗 Found URL in task: https://news.google.com, adding as initial action...
INFO     [Agent] 🎯 Task: Open news.google.com
INFO     [Agent] Starting a browser-use agent with version 0.11.9, with provider=google and model=gemini-3-flash-preview
INFO     [Agent]   ▶️   navigate: url: https://news.google.com, new_tab: False
WARNING  [BrowserSession] ⚠️ Page readiness timeout (4.0s, 4259ms) for https://news.google.com
INFO     [tools] 🔗 Navigated to https://news.google.com
INFO     [Agent] 

INFO     [Agent] 📍 Step 1:
INFO     [Agent]   👍 Eval: Successfully navigated to news.google.com. Verdict: Success
INFO     [Agent]   🧠 Memory: Navigated to Google News. The page is fully loaded and visible.
INFO     [Agent]   🎯 Next goal: The task is completed, so I will call the done action.
INFO     [Agent]   ▶️   done: text: I have successfully opened news.google.com., success: True, files_to_display: []
INFO     [Agent] 📋 Plan updated with 1 steps
INFO     [Agent] 
📄  Final Result: 
I have successfully opened news.google.com.


INFO     [Agent] ✅ Task completed successfully

 👤 New task or "q" to quit: search for news
INFO     [Agent] 🎯 Task: New task: search for news
INFO     [Agent] 

INFO     [Agent] 📍 Step 2:
INFO     [Agent]   👍 Eval: Successfully navigated to news.google.com in the previous step. Verdict: Success
INFO     [Agent]   🧠 Memory: I am on news.google.com. I need to perform a search as per the follow-up request.
INFO     [Agent]   🎯 Next goal: Search for 'latest news' using the search bar.
INFO     [Agent]   ▶️  [1/2] input: index: 7, text: latest news, clear: True
INFO     [BrowserSession] ⌨️ Typed "latest news" into element with index 7
INFO     [Agent]   ▶️  [2/2] click: index: 41
INFO     [tools] 🖱️ Clicked button role=button aria-label=Search
INFO     [Agent] 📋 Plan updated with 3 steps
INFO     [Agent] 

INFO     [Agent] 📍 Step 3:
INFO     [Agent]   👍 Eval: Successfully performed the search for 'latest news' and navigated to the results page. Verdict: Success
INFO     [Agent]   🧠 Memory: Navigated to news.google.com and performed a search for 'latest news'. The search results page is now loaded with various news articles.
INFO     [Agent]   🎯 Next goal: The task is complete, so I will call the done action.
INFO     [Agent]   ▶️   done: text: I have successfully searched for 'latest news' on Google News. The search results include articles from various international and local sources, such ..., success: True, files_to_display: []
INFO     [Agent] 📋 Plan updated with 3 steps
INFO     [Agent] 
📄  Final Result: 
I have successfully searched for 'latest news' on Google News. The search results include articles from various international and local sources, such as the ASEAN Main Portal, BBC, and The New York Times.


INFO     [Agent] ⚠️  Simple judge overriding success to failure: The agent reported that it performed the search but did not provide any actual news headlines or content as part of the response, making the result incomplete.
INFO     [Agent] 
INFO     [Agent] Did the Agent not work as expected? Let us fix this!
INFO     [Agent]    Open a short issue on GitHub: https://github.com/browser-use/browser-use/issues

 👤 New task or "q" to quit: click on Indonesia
INFO     [Agent] 🎯 Task: New task: click on Indonesia
INFO     [Agent] 

INFO     [Agent] 📍 Step 4:
INFO     [Agent]   👍 Eval: The search for 'latest news' was successful, and the results page is displayed. Verdict: Success
INFO     [Agent]   🧠 Memory: Successfully searched for 'latest news'. Now moving to the next task of clicking on the 'Indonesia' section in Google News.
INFO     [Agent]   🎯 Next goal: Click on the 'Indonesia' tab to view news related to Indonesia.
INFO     [Agent]   ▶️   click: index: 540
INFO     [tools] 🖱️ Clicked a role=tab "Indonesia" aria-label=Indonesia
INFO     [Agent] 📋 Plan updated with 3 steps
INFO     [Agent] 

INFO     [Agent] 📍 Step 5:
INFO     [Agent]   👍 Eval: Successfully clicked on the 'Indonesia' tab and navigated to the Indonesia news section. Verdict: Success
INFO     [Agent]   🧠 Memory: Navigated to news.google.com, searched for 'latest news', and then successfully switched to the 'Indonesia' news section. The page now shows news relevant to Indonesia.
INFO     [Agent]   🎯 Next goal: The task is complete. I will now signal completion.
INFO     [Agent]   ▶️   done: text: I have successfully navigated to Google News, performed a search for 'latest news', and then clicked on the 'Indonesia' section as requested. The brow..., success: True, files_to_display: []
INFO     [Agent] 📋 Plan updated with 3 steps
INFO     [Agent] 
📄  Final Result: 
I have successfully navigated to Google News, performed a search for 'latest news', and then clicked on the 'Indonesia' section as requested. The browser is now displaying the Indonesia news page.


INFO     [Agent] ✅ Task completed successfully

 👤 New task or "q" to quit: q
INFO     [BrowserSession] 📢 on_BrowserStopEvent - Calling reset() (force=True, keep_alive=True)
INFO     [BrowserSession] [SessionManager] Cleared all owned data (targets, sessions, mappings)
INFO     [BrowserSession] ✅ Browser session reset complete
INFO     [BrowserSession] ✅ Browser session reset complete
```