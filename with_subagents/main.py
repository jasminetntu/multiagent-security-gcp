import asyncio

# Import the main agent
from main_agent.agent import root_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

# ===== PART 1: Initialize In-Memory Session Service =====
# Using in-memory storage for this example (non-persistent)
session_service = InMemorySessionService()


# ===== PART 2: Define Initial State =====
# This will be used when creating a new session
initial_state = {
    "key": "",
    "vulnerabilities": {},
    "interaction_history": [],
}


async def main_async():
    # Setup constants
    APP_NAME = "Security Agent"
    USER_ID = "security agent"

    # ===== PART 3: Session Creation =====
    # Create a new session with initial state
    # *** FIX: Await the create_session call ***
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id  # Now new_session is the actual session object
    print(f"Created new session with ID: {SESSION_ID}") # Added SESSION_ID to print

    # ===== PART 4: Agent Runner Setup =====
    # Create a runner with the main customer service agent
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nWelcome to Security Agent!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Update interaction history with the user's query
        # Ensure SESSION_ID is valid before using it here
        if SESSION_ID:
            add_user_query_to_history(
                session_service, APP_NAME, USER_ID, SESSION_ID, user_input
            )

            # Process the user query through the agent
            await call_agent_async(runner, USER_ID, SESSION_ID, user_input)
        else:
            print("Error: Session ID not available. Cannot process query.")

    # ===== PART 6: State Examination =====
    # Show final session state
    if SESSION_ID: # Check if SESSION_ID was successfully created
        final_session = session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print("\nFinal Session State:")
        for key, value in final_session.state.items():
            print(f"{key}: {value}") # Corrected f-string formatting for clarity
    else:
        print("\nNo session was successfully created to display final state.")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()