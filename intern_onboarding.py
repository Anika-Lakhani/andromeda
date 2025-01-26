import openai
import json
import datetime
import os
from typing import Dict, List, Optional
from openai import OpenAI

# Configure OpenAI API
try:
    with open('apikey.txt', 'r') as f:
        openai.api_key = f.read().strip()
except FileNotFoundError:
    print("Error: apikey.txt file not found. Please create this file with your OpenAI API key.")
    exit(1)
except Exception as e:
    print(f"Error reading API key: {str(e)}")
    exit(1)

class InternOnboarding:
    def load_company_info(self) -> str:
        """
        Load company information from company_info.txt file
        """
        try:
            with open('company_info.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Error: company_info.txt file not found. Please create this file with company information.")
            exit(1)
        except Exception as e:
            print(f"Error reading company information: {str(e)}")
            exit(1)

    def load_company_summary(self) -> str:
        """
        Load company summary from company_summary.txt file
        """
        try:
            with open('company_summary.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Error: company_summary.txt file not found. Please create this file with company summary.")
            exit(1)
        except Exception as e:
            print(f"Error reading company summary: {str(e)}")
            exit(1)

    def load_tools_summary(self) -> str:
        """
        Load tools summary from tools_summary.txt file
        """
        try:
            with open('tools_summary.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Error: tools_summary.txt file not found. Please create this file with tools summary.")
            exit(1)
        except Exception as e:
            print(f"Error reading tools summary: {str(e)}")
            exit(1)

    def load_expectations_summary(self) -> str:
        """
        Load expectations summary from expectations_summary.txt file
        """
        try:
            with open('expectations_summary.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Error: expectations_summary.txt file not found. Please create this file with expectations summary.")
            exit(1)
        except Exception as e:
            print(f"Error reading expectations summary: {str(e)}")
            exit(1)

    def load_specific_responsibilities(self, intern_type: str) -> str:
        """
        Load responsibilities based on intern type from specific txt files
        """
        filename = {
            "Marketing": "marketing_responsibilities.txt",
            "Tech": "tech_responsibilities.txt",
            "Operations": "ops_responsibilities.txt",
            "AI": "ai_responsibilities.txt",
            "I don't know": "intern_responsibilities.txt"
        }.get(intern_type)

        try:
            with open(filename, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: {filename} file not found. Please create this file with {intern_type} responsibilities.")
            exit(1)
        except Exception as e:
            print(f"Error reading {intern_type} responsibilities: {str(e)}")
            exit(1)

    def load_external_tools(self) -> str:
        """
        Load external tools information from external_tools.txt file
        """
        try:
            with open('external_tools.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Error: external_tools.txt file not found. Please create this file with tools information.")
            exit(1)
        except Exception as e:
            print(f"Error reading external tools information: {str(e)}")
            exit(1)

    def load_project_expectations(self) -> str:
        """
        Load project expectations from project_expectations.txt file
        """
        try:
            with open('project_expectations.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Error: project_expectations.txt file not found. Please create this file with project expectations.")
            exit(1)
        except Exception as e:
            print(f"Error reading project expectations: {str(e)}")
            exit(1)

    def __init__(self):
        # Load API key and initialize client
        try:
            with open('apikey.txt', 'r') as f:
                api_key = f.read().strip()
            self.client = OpenAI(api_key=api_key)
        except FileNotFoundError:
            print("Error: apikey.txt file not found. Please create this file with your OpenAI API key.")
            exit(1)
        except Exception as e:
            print(f"Error reading API key: {str(e)}")
            exit(1)

        # Load all information files
        self.company_info = self.load_company_info()
        self.company_summary = self.load_company_summary()
        self.responsibilities_info = self.load_specific_responsibilities("I don't know")
        self.tools_info = self.load_external_tools()
        self.tools_summary = self.load_tools_summary()
        self.project_info = self.load_project_expectations()
        self.expectations_summary = self.load_expectations_summary()
        
        self.conversation_history = []
        self.topics = {
            1: "Company Overview",
            2: "Intern Responsibilities",
            3: "Tools and Technologies",
            4: "Project Expectations"
        }

    def get_ai_response(self, prompt: str, include_company_info: bool = True) -> str:
        """
        Get response from OpenAI API with detailed error handling
        """
        try:
            full_prompt = prompt
            if include_company_info:
                full_prompt = f"Company Information:\n{self.company_info}\n\n{prompt}"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except openai.APIError as e:
            if 'insufficient_quota' in str(e):
                return ("Error: Your project has reached its API quota limit.\n"
                       "Please check your project settings at https://platform.openai.com/\n"
                       "Ensure that:\n"
                       "1. Your project has billing properly set up\n"
                       "2. You have sufficient credits/quota\n"
                       "3. The API key is active and not restricted")
            elif 'invalid_api_key' in str(e):
                return ("Error: Invalid API key.\n"
                       "Please verify that your API key is correct and active in your project settings.")
            elif 'rate_limit' in str(e):
                return ("Error: Too many requests.\n"
                       "Please wait a moment before trying again.")
            else:
                return f"OpenAI API Error: {str(e)}"
        except Exception as e:
            return (f"Unexpected error: {str(e)}\n"
                   "If this persists, please contact technical support.")

    def company_overview(self) -> str:
        """
        Provides company overview and handles follow-up questions
        """
        print(self.company_summary)
        
        while True:
            follow_up = input("\nWould you like to ask a follow-up question about Andromeda Protocol? (Y/N): ").strip().upper()
            if follow_up == 'Y':
                question = input("\nWhat would you like to know? ")
                prompt = f"Using the provided company information, please answer this question: {question}"
                return self.get_ai_response(prompt)
            elif follow_up == 'N':
                return ""
            else:
                print("Please enter Y or N.")

    def intern_responsibilities(self) -> str:
        """
        Provides role-specific responsibilities and handles follow-up questions
        """
        intern_types = {
            1: "Marketing",
            2: "Tech",
            3: "Operations",
            4: "AI",
            5: "I don't know"
        }

        # Display intern type options
        print("\nWhat type of intern are you?")
        for key, value in intern_types.items():
            print(f"{key}. {value}")

        # Get valid intern type selection
        while True:
            try:
                choice = int(input("\nEnter your choice (1-5): "))
                if 1 <= choice <= 5:
                    intern_type = intern_types[choice]
                    break
                print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        # Load and display role-specific responsibilities
        role_responsibilities = self.load_specific_responsibilities(intern_type)
        print(f"\n{role_responsibilities}")
        
        # Handle follow-up questions
        while True:
            follow_up = input("\nWould you like to ask a follow-up question about intern responsibilities? (Y/N): ").strip().upper()
            if follow_up == 'Y':
                question = input("\nWhat would you like to know? ")
                prompt = (
                    f"Using both the intern responsibilities information and company information provided, "
                    f"please answer this question about the {intern_type} internship role: {question}\n\n"
                    f"Role-Specific Responsibilities:\n{role_responsibilities}\n\n"
                    f"Company Information:\n{self.company_info}"
                )
                return self.get_ai_response(prompt)
            elif follow_up == 'N':
                return ""
            else:
                print("Please enter Y or N.")

    def tools_and_technologies(self) -> str:
        """
        Provides tools and technologies recommendations based on intern type
        """
        intern_types = {
            1: "Marketing",
            2: "Tech",
            3: "Operations",
            4: "AI",
            5: "I don't know"
        }

        # Display intern type options
        print("\nWhat type of intern are you?")
        for key, value in intern_types.items():
            print(f"{key}. {value}")

        # Get valid intern type selection
        while True:
            try:
                choice = int(input("\nEnter your choice (1-5): "))
                if 1 <= choice <= 5:
                    intern_type = intern_types[choice]
                    break
                print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        # Construct prompt based on intern type
        if intern_type == "I don't know":
            prompt = (
                "Based on the following information about our company, intern roles, and available tools:\n\n"
                f"Company Info:\n{self.company_info}\n\n"
                f"Intern Roles:\n{self.responsibilities_info}\n\n"
                f"Tools:\n{self.tools_info}\n\n"
                "Please provide a general overview of useful tools and technologies that would be helpful "
                "for any intern role at the company. Focus on common tools that could benefit anyone "
                "joining the team."
            )
        else:
            prompt = (
                "Based on the following information about our company, intern roles, and available tools:\n\n"
                f"Company Info:\n{self.company_info}\n\n"
                f"Intern Roles:\n{self.responsibilities_info}\n\n"
                f"Tools:\n{self.tools_info}\n\n"
                f"Please suggest specific tools and technologies that would be most helpful for a {intern_type} "
                f"intern at the company. Focus on tools that align with the {intern_type} role's responsibilities "
                "and would help them succeed in their position."
            )

        # Get and display initial response
        response = self.get_ai_response(prompt)
        print(f"\nRecommended Tools and Technologies:\n{response}")

        # Handle follow-up questions
        while True:
            follow_up = input("\nWould you like to ask a follow-up question about tools and technologies? (Y/N): ").strip().upper()
            if follow_up == 'Y':
                question = input("\nWhat would you like to know? ")
                follow_up_prompt = (
                    f"Based on the previous tools and technologies discussion for a {intern_type} intern, "
                    f"please answer this follow-up question: {question}"
                )
                return self.get_ai_response(follow_up_prompt)
            elif follow_up == 'N':
                return ""
            else:
                print("Please enter Y or N.")

    def project_expectations(self) -> str:
        """
        Provides project expectations overview and handles follow-up questions
        """
        print(self.expectations_summary)
        
        while True:
            follow_up = input("\nWould you like to ask a follow-up question about project expectations? (Y/N): ").strip().upper()
            if follow_up == 'Y':
                question = input("\nWhat would you like to know? ")
                prompt = (
                    "Based on the following information:\n\n"
                    f"Company Information:\n{self.company_info}\n\n"
                    f"Intern Responsibilities:\n{self.responsibilities_info}\n\n"
                    f"Tools and Technologies:\n{self.tools_info}\n\n"
                    f"Project Expectations:\n{self.project_info}\n\n"
                    f"Please answer this question about project expectations: {question}"
                )
                return self.get_ai_response(prompt)
            elif follow_up == 'N':
                return ""
            else:
                print("Please enter Y or N.")

    def save_conversation(self):
        """
        Save conversation history to a JSON file
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"onboarding_conversation_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=4)
            return f"Conversation saved to {filename}"
        except Exception as e:
            return f"Error saving conversation: {str(e)}"

    def display_menu(self):
        """
        Display the main menu options
        """
        print("\n=== Intern Onboarding Guide ===")
        for key, value in self.topics.items():
            print(f"{key}. {value}")
        print("5. Save Conversation")
        print("6. Exit")

    def handle_topic(self, choice: int) -> Optional[str]:
        """
        Handle user topic selection
        """
        topic_handlers = {
            1: self.company_overview,
            2: self.intern_responsibilities,
            3: self.tools_and_technologies,
            4: self.project_expectations
        }
        
        if choice in topic_handlers:
            response = topic_handlers[choice]()
            if response:  # Only append to history if there's a response (follow-up question was asked)
                self.conversation_history.append({
                    "topic": self.topics[choice],
                    "response": response,
                    "timestamp": datetime.datetime.now().isoformat()
                })
            return response
        return None

def main():
    onboarding = InternOnboarding()
    
    while True:
        try:
            onboarding.display_menu()
            choice = int(input("\nEnter your choice (1-6): "))
            
            if choice == 6:
                print("Thank you for using the Intern Onboarding Guide!")
                break
            elif choice == 5:
                result = onboarding.save_conversation()
                print(result)
            elif 1 <= choice <= 4:
                response = onboarding.handle_topic(choice)
                if response:
                    print(f"\nResponse:\n{response}")
            else:
                print("Invalid choice. Please select a number between 1 and 9.")
                
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
