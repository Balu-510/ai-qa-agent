def parse_instruction(text):
    commands = []
    lines = text.lower().split("\n")

    for line in lines:

        # OPEN
        if "open" in line:
            if "youtube" in line:
                url = "https://www.youtube.com"
            elif "google" in line:
                url = "https://www.google.com"
            elif "file://" in line:
                url = line.replace("open", "").strip()
            else:
                url = line.replace("open", "").strip()

            commands.append({"action": "open", "url": url})

        # SEARCH
        elif "search" in line:
            query = line.replace("search", "").strip()
            commands.append({"action": "search", "query": query})

        # PLAY VIDEO
        elif "play" in line:
            query = line.replace("play", "").strip()
            commands.append({"action": "play", "query": query})

        # LOGIN INPUT
        elif "username" in line:
            value = line.split()[-1]
            commands.append({"action": "type", "selector": "#username", "text": value})

        elif "password" in line:
            value = line.split()[-1]
            commands.append({"action": "type", "selector": "#password", "text": value})

        # CLICK
        elif "click" in line:
            commands.append({"action": "click", "selector": "#loginBtn"})

        # ASSERT
        elif "check" in line:
            expected = line.replace("check", "").strip()
            commands.append({"action": "assert", "text": expected})

    return commands