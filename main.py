from search import Search
import os

conf = "config.json"

search = Search(conf)
if not os.path.exists(conf):
    search.create_config()

search.root.mainloop()
