#SideBar Components
# st.sidebar.header("S&P500 Index")
# with st.sidebar:

#     st.session_state["ticker"] = ""


#     title = st.text_input("Enter a stock ticker (e.g., AAPL):", "AAPL", placeholder="Search for a symbol", max_chars=4, )
#     search = st.button("Search", type="primary")
#     #st.caption(":red[Ticker not found]")

#     options = ticker_dictionary().keys()
#     selected_sector = st.sidebar.pills('Ticker', options, selection_mode="single", )

#     if search and title:
#         st.session_state["ticker"] = title
#         obj = DataIngestion(st.session_state["ticker"])
#         df = obj.initiate_data_ingestion()
#         title = ""
#         #st.session_state.data_frame = df
#     elif selected_sector:
#         st.session_state["ticker"] = ticker_dictionary().get(selected_sector)
#         obj = DataIngestion(st.session_state["ticker"])
#         df = obj.initiate_data_ingestion()
#         selected_Sector = ""
#         #st.session_state.data_frame = df
