# Written By: Rachael Rogan
# A method that prints all the lines of Bate's Triangle and its prime factorization.

# Ref to get prime numbers https://www.geeksforgeeks.org/python-sympy-primefactors-method/

from sympy import primefactors

def create_triangle(numRows):
    triangle = []
    for row in range(numRows):
        triangle.append([])
        if row % 2 == 0:
            triangle[row].append(0)
        else:
            triangle[row].append(1)
        
        if row > 1 :
            for i in range(len(triangle[row-1]) - 1):
                triangle[row].append(triangle[row-1][i] + triangle[row-1][i+1])

        if row > 0:
            triangle[row].append(row)
    return triangle

def print_triangle(triangle):
    left_padded_spaces = 1
    string_rows = [] # look up how to append to the front of a list

    # Print the bottom row based on the spaces needed 
    # for the second to last row
    last_row = triangle[len(triangle)-1]
    bottom_string = ""
    for e in range(len(last_row)): # for each entry in the bottom row
        bottom_string += str(last_row[e])
        # See how many characters are in the row above
        for c in str(triangle[len(triangle)-2][e if e < len(triangle[len(triangle)-2]) else e-1]):
            bottom_string += " "
    string_rows.append(bottom_string)

    row_string = ""

    for r in range(len(triangle[:len(triangle)-2]), -1, -1): # starting from the second to last row, we make strings going up
        row = triangle[r]
        last_blanks = []
        row_string = " "*left_padded_spaces
        row_string += str(row[0])
        next_start = 0
        if len(row) > 1:
            for entry in row[1:]: # we already printed the first number, so we start with the second
                found_num = False
                row_after = string_rows[0][left_padded_spaces+1+next_start:] # look at the row below in the triangle
                count_spaces = 0
                blank_spaces = 0
                for c in row_after:
                    if(c == " "):
                        if(found_num == False):
                            count_spaces += 1
                            blank_spaces += 1
                        else:
                            break
                    else:
                        found_num = True
                        count_spaces += 1
                spaces = " "*count_spaces
                row_string += spaces
                row_string += str(entry)
                next_start += len(spaces+ str(entry))
                last_blanks.append(spaces)
        left_padded_spaces +=1
        string_rows.insert(0, row_string)

    for row in string_rows:
        print(row)

def get_prime_factors(num):
    primes = []
    prime_list = []
    for p in primefactors(num):
        reduced_num = num
        while(reduced_num%p == 0):
            prime_list.append(p)
            reduced_num /= p
    if not prime_list:
        return num
    else:
        return prime_list

def get_prime_triangle(triangle):
    new_triangle = []
    for row in triangle:
        new_row = []
        for entry in row:
            new_row.append(get_prime_factors(entry))
        new_triangle.append(new_row)
    return new_triangle

def condense_primes(prime_triangle):
    new_triangle = []
    for row in prime_triangle:
        new_row = [] # where we will keep our strings
        for entry in row: # each of the elements is either a list of prime numbers or a single value
            if isinstance(entry, list):
                seen_nums = {}
                primes_str = ""
                for num in entry:
                    if num in seen_nums:
                        seen_nums[num] += 1
                    else:
                        seen_nums[num] = 1
                for prime in seen_nums:
                    primes_str += str(prime) + "," + str(seen_nums[prime])
                    if len(seen_nums) > 1 :
                        primes_str += ","
                new_row.append(primes_str)
            else:
                new_row.append(entry)
        new_triangle.append(new_row)
    return new_triangle

# https://codepen.io/ArtBlue/pen/EPERBK for general HTML format (I populated this with Bate's triangle)
def create_html_triangle(triangle, caption, add_superscripts):
    all_html = "<table border = '0' cellspacing='1' cellpadding='3'> "
    all_html += "<H3><BR>{}</H3>".format(caption)
    row = ""
    string = ""
    num_columns = len(triangle[len(triangle)-1])*2 - 2
    padded_blanks = int(num_columns / 2)
    for row in triangle:
        all_html += "<tr>"
        all_html = add_blank_cols(all_html, padded_blanks)
        # parse through all the column entries of the triangle
        for entry in row:
            all_html = place_char(all_html, entry, add_superscripts)
            all_html = place_char(all_html, " ", False)
        all_html = add_blank_cols(all_html, padded_blanks - 1)
        all_html += "</tr>"
        padded_blanks -= 1

    all_html += "</table>"
    return all_html

def add_blank_cols(htmlstr, num_blanks):
    for i in range(num_blanks):
        htmlstr += "<td align='center'></td>"
    return htmlstr

# Add superscript abilities
def place_char(htmlstr, c, add_superscripts):
    if add_superscripts:
        chars = str(c).split(",")
        if len(chars) > 2:
            i = 0
            maxIndexLoop = len(chars)-2
            htmlstr += "<td align='center'>"
            while i < maxIndexLoop :
                htmlstr += "{number}<sup>{exp}</sup>".format(number = chars[i], exp = chars[i+1])
                i += 2
            htmlstr += "</td>"
        elif len(chars) == 2:
            htmlstr += "<td align='center'>{number}<sup>{exp}</sup></td>".format(number = chars[0], exp = chars[1])
        else:
            htmlstr += "<td align='center'>{}</td>".format(c)
    else:
        htmlstr += "<td align='center'>{}</td>".format(c)
    return htmlstr

def main():

    numRows = int(input("Please enter the number of rows you want to see (0 to exit): "))
    triangle = create_triangle(int(numRows))
    triangle2 = condense_primes(get_prime_triangle(triangle))
    
    ###############################
    # Ref: https://programminghistorian.org/en/lessons/output-data-as-html-file 
    import webbrowser

    f = open('triangle.HTML','w')

    message = create_html_triangle(triangle, "Original", False)
    print("---------------------------------------")
    message += create_html_triangle(triangle2, "Prime Factorization", True)

    f.write(message)
    f.close()

    webbrowser.open_new_tab('triangle.html')
    ###################################

if __name__ == "__main__":
    main()