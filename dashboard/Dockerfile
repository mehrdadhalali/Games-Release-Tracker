FROM python:3.11

WORKDIR /dashboard

RUN mkdir pages
RUN mkdir .streamlit
RUN mkdir pages/utils


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords 

COPY functions.py .
COPY sl_queries.py . 
COPY .streamlit/config.toml ./.streamlit
COPY pages/Subscribe.py .
COPY pages/logo.png ./pages
COPY pages/Games.py ./pages
COPY pages/About.py ./pages
COPY pages/utils/subscribe_functions.py ./pages/utils
COPY Dashboard.py .


CMD [ "streamlit", "run" , "Dashboard.py" ]