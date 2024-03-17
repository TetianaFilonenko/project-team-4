import os

def print_ascii_art(ascii_art):
    # Get the terminal width
    terminal_width = os.get_terminal_size().columns

    # Calculate the number of spaces needed for centering
    left_padding = (terminal_width - max(len(line.strip()) for line in ascii_art.split('\n'))) // 2

    # Print ASCII art with proper padding for centering
    for line in ascii_art.split('\n'):
        print(' ' * left_padding + line) 


logo = """
                                                     ***                                              
                                                   ***                                              
                                                  ****                                              
                                                  ***                                               
                                                 ***                                                
                                %%              ***         %%                                      
                                %%              ***         %%                                      
                                %%             ***          %%                                      
                                %%            ****          %%                                      
                             %%%%            *#  **          %%%                                    
                                %%          * *  ***        %%                                      
                                %%         * *   ***        %%                                      
                                %%        * **   ***        %%                                      
                                %%       ** **  ****        %%                                      
                                         *      ****                                                
                                         *     ****                                                 
                                         *   *****                                                  
                                          ******                                                    
                                                                                                    
 **  ***          **                               *******                **                        
 ** **    ****    ******    *****   ****    ** ** **     *   ****     ******   ****    * *** #****  
 ****    **   **  ***  ** **  #**  **   **  ***   **       **   **  ***   ** ***   **  ***  **   ** 
 *****   **   **  **   **    **    *******  **    **       **    ** **    ** ********  **    ****** 
 **  *** **   **  ***  **  ***  ** **  ***  **    **    ** ***  **  ***  *** ***   **  **   **   ***
 **    *  ****    * ****   ******   *** **  **      ****     ****     *** *    ****    *     ***** 
 """

# Print the ASCII art
# print_ascii_art(logo)
