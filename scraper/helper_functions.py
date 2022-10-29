def display_banner() -> None:
    banner = """
   oooooo   oooooo     oooo            .o8                                                                           
    `888.    `888.     .8'            "888                                                                           
     `888.   .8888.   .8'    .ooooo.   888oooo.   .oooo.o  .ooooo.  oooo d8b  .oooo.   oo.ooooo.   .ooooo.  oooo d8b 
      `888  .8'`888. .8'    d88' `88b  d88' `88b d88(  "8 d88' `"Y8 `888""8P `P  )88b   888' `88b d88' `88b `888""8P 
       `888.8'  `888.8'     888ooo888  888   888 `"Y88b.  888        888      .oP"888   888   888 888ooo888  888     
        `888'    `888'      888    .o  888   888 o.  )88b 888   .o8  888     d8(  888   888   888 888    .o  888     
         `8'      `8'       `Y8bod8P'  `Y8bod8P' 8""888P' `Y8bod8P' d888b    `Y888""8o  888bod8P' `Y8bod8P' d888b    
                                                                                        888                          
                                                                                       o888o                         
                                                                                                                  
    
    """
    print(banner)

def display_introduction_text() -> str:
    intro = """
    Welcome to the Webscraper of Indeed.
    Type command to start Webscraper. 
    - "Jobtitle' to scrape indeed for that jobtitle. 
    - 'Find all' to scrape Indeed for all locations. 
    - 'Q' to quit. 
    """
    print(intro)