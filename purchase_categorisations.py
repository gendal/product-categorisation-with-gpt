### Richard G Brown
### 2023-11-19
### Simple script to demonstrate OpenAI Chat Completion API being used
### to categorise items as "OK to purchase" or "Not OK to purchase" by a child

from openai import OpenAI
import json

client = OpenAI()

prompt = """
  Imagine I am a parent and I want to protect my children from harm. 
  Here are some examples of things they should NOT be allowed to buy in a store without my permission: 
    sharp objects such as scissors; 
    products containing hazardous chemicals such as bleach; 
    high calorie foods such as sugary sodas.  
  Here are some examples of things they CAN buy without my permission: 
    fruit; very small packets of candy; 
    toys; 
    age-appropriate comics.   
  Respond with an RFC8259 compliant JSON response following this format without deviation.
    [{ "is_purchase_by_a_child_allowed": "true or false",
       "certainty": "how certain you are using a word such as 'high' or 'medium' and so forth",
       "explanation": "your reasoning"
    }]
"""

expected_fingerprint_to_detect_determinism_loss = "fp_a24b4d720c" # As observed for gpt-4-1106-preview on 2023-11-19

def check_purchase_validity(client, item):
    """
      :param client: OpenAI client object
      :param item: An item that a child would like to purchase
      :returns: {
          "is_purchase_by_a_child_allowed": "true or false",
          "certainty": "confidence level",
          "explanation": "explanation"
        }
    """
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview", # Specifically designed to reliably output JSON
        response_format={ "type": "json_object" },
        #seed = 1, # To test deterministic output. Seems to be very slow if set
        messages=[
          {"role":
             "system",
           "content":
             prompt
           },
          {"role":
             "user",
           "content":
             "Is the child allowed to purchase {}".format(item)
           }
        ]
    )
    fingerprint = completion.system_fingerprint
    if(fingerprint != expected_fingerprint_to_detect_determinism_loss):
      print("WARNING: Fingerprint changed! This may be due to a change in the model. Please check the output.")
      print("  Old fingerprint: {}".format(expected_fingerprint_to_detect_determinism_loss))
      print("  New fingerprint: {}".format(fingerprint))
    response = completion.choices[0].message
    responseDict = json.loads(response.content)
    return responseDict

with open('items.txt') as items_file:
  items = [line.rstrip('\n') for line in items_file]

for item in items:
    print("Checking: {}".format(item))
    result = check_purchase_validity(client, item)
    print("  OK to purchase? {}. (Confidence: {})".format(result["is_purchase_by_a_child_allowed"], result["certainty"]))
    print("    Explanation: {}".format(result["explanation"]))
    print()
