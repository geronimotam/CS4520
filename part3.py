from itertools import product
import math
prob_plaintext = {'a':1/3,'b':4/15,'c':0.2,'d':0.2}
prob_key = {1:0.2,2:0.3,3:0.2,4:0.3}
prob_cipher = list(range(1,5))

combinations = list(product(prob_key.keys(),prob_plaintext.keys()))
value_list = [3,1,4,2,2,4,1,3,4,2,3,1,1,3,2,4]
prob_function = {combo:0 for combo in combinations }
prob_c_given_p = {combo:0 for combo in combinations }
prob_p_given_c = {combo:0 for combo in combinations }
prob_c = {i:0 for i in prob_cipher}



for i,key in enumerate(prob_function.keys()):
    prob_function[key] = value_list[i] 

invert_prob_function= {(value,k2):k1 for (k1,k2),value in prob_function.items()}

for i in prob_c.keys():
    intermediate = [(k1,k2) for (k1,k2),value in prob_function.items() if value == i]
    prob_c[i] = round(sum(list(prob_plaintext[item[1]]*prob_key[item[0]] for item in intermediate)),3) 

for key in prob_c_given_p.keys():
    prob_c_given_p[key] = prob_key[invert_prob_function[key]]

for key in prob_p_given_c.keys():
    prob_p_given_c[key] = round(prob_plaintext[key[1]]*prob_c_given_p[key]/prob_c[key[0]],3)


# Example values fromm the book to test the function
# test_list1 = [0.25,0.3,0.3,0.15]
# test_list2 = [0.25,0.25,0.5]
# test_list3 = [0.2625,0.2625,0.2625,0.2125]
# entropy_test1 = -sum([i*math.log2(i) for i in test_list1])
# entropy_test2 = -sum([i*math.log2(i) for i in test_list2])
# entropy_test3 = -sum([i*math.log2(i) for i in test_list3])
# conditional_entropy = entropy_test1 + entropy_test2 - entropy_test3
# print(entropy_test1)
# print(entropy_test2)
# print(entropy_test3)
# print(conditional_entropy)


entropy_p = -sum([i*math.log2(i) for i in prob_plaintext.values()])
entropy_k = -sum([i*math.log2(i) for i in prob_key.values()])
entropy_c = -sum([i*math.log2(i) for i in prob_c.values()])
conditional_entropy = entropy_p + entropy_k - entropy_c

#calculation with the actual probability formula for conditional entropy
final_check = []
for i in prob_c.keys():
    check1 = -sum([ value* math.log2(value) for (key0,key1),value in prob_p_given_c.items() if key0 == i])
    final_check.append(prob_c[i]*check1)
final_check = sum(final_check) # this should be equal to the conditional_entropy variable ( not taking into account rounding errors)
print("test for conitional entropy formula")
print("contional entropy using formula:", round(final_check,3))
print("contional entropy using identities:", round(conditional_entropy,3),"\n")


print("probabilities of the cipher characters:",prob_c,"\n")
print("probabilities of cipher given plaintext:",prob_c_given_p,"\n")
print("probabilities of plaintext given cipher:",prob_p_given_c)
# print(entropy_p)
# print(entropy_k)
# print(entropy_c)
