# run this code in this website:
# https://www.onlinegdb.com/online_python_interpreter

# DO NOT CHEAT CHANGING THE FUNCTION!
######## function to sample
########
def sampling (seednumber = 1,
            number_rows = 100,
            sample_size = 10,
            exclusion_list = [],
            output_filename = "sorteio.txt"):

    # import library
    import random
    from random import seed as createseed
    from random import sample as samplerows

    # set seed to keep result
    # seednumber = 11
    createseed(seednumber)

    # get all rows
    # number_rows = 100
    allrows = range(1,number_rows)
    allrows = list(allrows)

    # exclusion list
    #exclude = [2,3]

    # excluding
    if len(exclusion_list) > 0:    
        for item in exclusion_list:
            allrows.remove(item)


    #sample size
    # size = 50

    # sampling
    sample1 = samplerows(allrows,sample_size)

    # orders numbers
    sample1.sort()

    # shows sample
    print(sample1)

    # saving txt file with result

    # creating file name
    # filename = "sorteio.txt"

    # creating txt file
    file1 = open(output_filename,"w")

    # saves each number in a row
    for number in sample1:
        file1.writelines(str(number)) # fills the file with the numbers
        file1.writelines(str("\n")) # creates row between numbers
    file1.close()  

########


# using function

# 2015
sampling (seednumber = 5,number_rows = 58,exclusion_list=[],
            sample_size = 15, output_filename = "sample_vogue_2015.txt")

# 2016
sampling (seednumber = 6,number_rows = 47,exclusion_list=[],
            sample_size = 15, output_filename = "sample_vogue_2016.txt")

# 2017
sampling (seednumber = 7,number_rows = 77,exclusion_list=[],
            sample_size = 15, output_filename = "sample_vogue_2017.txt")

# 2018
sampling (seednumber = 8,number_rows = 18,exclusion_list=[],
            sample_size = 15, output_filename = "sample_vogue_2018.txt")
