import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

st.title("Generator przypadków medycznych")


def generate_response(prompt_template, **kwargs):
    """
    Generates a response from the OpenAI API using a prompt template with placeholders.

    Args:
        prompt_template (str): The prompt template with placeholders in curly braces, e.g. "Write a {length} paragraph about {topic}."
        **kwargs: Keyword arguments to replace the placeholders in the prompt template.

    Returns:
        str: The generated response from the OpenAI API.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = prompt_template.format(**kwargs)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś lekarzem który przygotowuje testy dla studentów"},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content


pacjent = st.text_area("Wprowadź krótki opis pacjenta")
okoliczności = st.text_area("Wprowadź krótki opis okoliczności w których pacjent trafił do szpitala")
objawy = st.text_area("Wprowadź krótki opis objawów które występują u pacjenta")
diagnostyka = st.text_area("Wprowadź krótki opis diagnostyki jaką przeprowadzono")

cel_testu = st.selectbox("Cel testu", ["pytanie o kolejną czynność diagnostyczną", "pytanie o rozpoznanie choroby", "pytanie o lek który należy podać"])

if st.button("Generuj przykład"):
    response = generate_response(
        prompt_template=f"""
        Pacjent to {pacjent}. Choroba wystąpiła w okolicznościach {okoliczności}. Objawy u pacjenta to {objawy}. 
        Pacjentowi zrobiono badania {diagnostyka}. 
        
        Przygotuj opis przypadku medycznego korzystając z powyższych informacji. Posłuż się przykładami podanymi niżej. Po opisie przypadku medycznego,
        przygotuj test wyobru z czterema opcjami odpowiedzi. Pytania mają dotyczyć {cel_testu}. Pytania mają być trudne. Zaznacz poprawną odpowiedź.
        Przygotowywany test dotyczy nauki neurologii, w opisie przypadku lub pytaniach możesz uwzględnić informacje związane z neurologią, takie jak
        nazwy chorób, objawy, diagnostyka, leczenie, profilaktyka, itp. charakterystyczne dla neurologii.
        
        Przykłady przypadków i testów:
        
        Przypadek 1: 
        Chory lat 76 został przyjęty do SOR z powodu wystąpienia nagłego silnego bólu głowy, nudności i wymiotów. 
        Objawy wystąpiły około 30 minut przed przyjęciem do SOR. Chorował na nadciśnienie tętnicze i cukrzycę typu 2.
        W badaniu neurologicznym stwierdzono Glasgow Coma Scale 13, sztywność karku na 4 palce, obustronnie objaw Kerniga, 
        niedowład połowiczy prawostronny ( 3 pkt w skali Lovetta) i prawostronnie objaw Babińskiego, zaburzenia mowy o charakterze afazji, 
        porażenie nerwu VI po stronie prawej,  tętno 110/min,  RR 150/95.
        Wykonano tomografię komputerową bez kontrastu , która nie wykazała odchyleń od stanu prawidłowego.
        Kolejnym badaniem, które należy wykonać w trybie pilnym jest:
        
        A) badanie metodą tomografii  rezonansu magnetycznego minimum z sekwencją DWI, FLAIR i gradient echo (T2*)
        B) ponowne badanie tomografii komputerowej z podaniem kontrastu jak najszybciej w tym samym dniu 
        C) (poprawne) badanie płynu mózgowo-rdzeniowego    
        D) ponowne badanie tomografii komputerowej minimum w odstępie 12 godzin, gdyż zmiany niedokrwienne mózgu z reguły nie uwidoczniają się w czasie 
        30 minut od udaru niedokrwiennego.

        Przypadek 2:
        Pacjent lat 68 został przyjęty do Szpitalnego Oddziału Ratunkowego z powodu drętwienia prawej połowy twarzy, prawych kończyn i prawej strony tułowia, 
        po 48 godzinach hospitalizacji objawy nadal utrzymywały się. Poza tym nie stwierdzano innych objawów w badaniu neurologicznym. RR przy przyjęciu 155/95 mmHg, 
        stężenie glukozy 130 mg/dl. W wywiadzie cukrzyca typu 2, i nadciśnienie tętnicze  innych schorzeń nie podaje. Najbardziej prawdopodobną przyczyną 
        wyżej wymienionych objawów ze strony układu nerwowego jest:

        A) Rzut stwardnienia rozsianego pod postacią niedoczulicy połowiczej
        B) Udar z zakresu unaczynienia tętnicy mózgu tylnej lewej 
        C) Początkowa faza ostrej zapalnej polineuropatii demielinizacyjnej (Guillaina-Barrego)
        D) (poprawne) Udar lakunarny mózgu

        Przypadek 3:
        Zespół ratowników medycznych przywiózł do SOR mieszkańca ośrodka dla bezdomnych z powodu bólów głowy z wymiotami i temperaturą 39,3 stopnie C. 
        W badaniu morfologii krwi obwodowej liczba krwinek białych wynosiła 19,7 G/L, stężenie CRP 86 mg/dl, glikemia 137 mg/dl, 
        a w wykonanym nakłuciu lędźwiowym pozyskano płyn mózgowo rdzeniowy z pleocytozą 56 000 komórek / mm3 i stężeniem białka 84 mg/dl. 
        Jakiego spodziewasz się stężenia glukozy w płynie m.rdz.

        A) 137 mg/dl
        B) 274 mg/dl
        C) (poprawne) 52 mg/dl
        D) 120 mg/dl
        E) glukoza nie wystepuje w p.m.r.

        Przypadek 4:
        Mężczyzna lat 43 przyjęty leczony od 6 lat na nadciśnienie tętnicze przyjęty został do oddziału udarowego z powodu niedowładu połowiczego lewostronnego. 
        W badaniu neurologicznym wykryto ponadto objaw Chvostka. 
        Podczas poszerzonego wywiadu ustalono, że chory przed przyjęciem do szpitala pomimo stosowania 3 leków hipotensyjnych miał wysokie wartości 
        ciśnienia tętniczego (rzędu 190/100). 
        Podczas pobytu szpitalnego badania laboratoryjne wykazały hipokalemię, która nie wyrównywała się pomimo przetaczania PWE. 
        Jaki plan dalszej diagnostyki przyjęłabyś/przyjąłbyś przede wszystkim w tym przypadku?

        A) (poprawne) TK nadnerczy
        B) oznaczenie stężenia wapnia 
        C) oznaczenie stężenia białka w dobowej zbiórce moczu 
        D) oznaczenie stężenia wapnia w dobowej zbiórce moczu 
        
        Przypadek 5:
        Pacjentka lat 32 została przywieziona do szpitala o godzinie 17.45 z objawami niedowładu połowiczego lewostronnego oraz prawostronnego 
        obwodowego porażenia nerwu twarzowego. Objawy wystąpiły nagle, tego dnia o godzinie 14.00. Dotychczas  chorowała na migrenę, leków nie pobierała. 
        Ciśnienie krwi 160/80 mmHg, stężenie glukozy 110 mg/dl. 
        W badaniu tomografii rezonansu magnetycznego z odchyleń stwierdzono jedynie w badaniu dyfuzji  (DWI - diffusion-weighted imaging)  
        ograniczenie dyfuzji w obrębie mostu po stronie prawej. 
        Prawidłowym postępowaniem w takiej sytuacji jest:
        
        A) (poprawne) Podanie jak najszybciej rekombinowanego aktywatora plazminogenu (Actylise) w dawce 0,9 mg/kg we wlewie dożylnym w ciągu 1 godziny
        B) Podanie jak najszybciej kwasu acetylosalicylowego doustnie w dawce 300 mg/dobę
        C) Ze względu na wystąpienie obwodowego porażenia nerwu twarzowego u młodej kobiety rozpoznanie udaru mózgu jest bardzo wątpliwe 
        i należy odroczyć decyzje terapeutyczne do czasu wykonania dalszych badań (m.in. w kierunku procesów zapalnych).
        D) Ze względu na wystąpienie obwodowego porażenie nerwu twarzowego podanie jak najszybciej metyloprednizolonu (Solu-Medrol) w 
        dawce od 500 do 1000 mg na dobę we wlewie dożylnym.
        E) Ze względu na lokalizację zmiany w pniu mózgu wskazane jest jedynie jak najszybsze podanie kwasu acetylosalicylowego doustnie w 
        dawce 300 mg/dobę, oraz  wykonanie badania tomografii komputerowej głowy i w przypadku uwidocznienia zmian rozważenie leczenia 
        rekombinowanym aktywatorem plazminogenu (Actylise).
        
        Napisz tylko i wyłącznie opis przypadku medycznego oraz jeden zestaw pytań. Kieruj się podanymi informacjami o pacjencie, okolicznościach i objawach.
        Możesz rozszerzyć opis pzypadku i dodać szczegóły które sprawią, że przypadek będzie bardziej interesujący i trudniejszy do rozwiązania.
        """,
        pacjent=pacjent,
        okolicznosci=okoliczności,
        objawy=objawy,
        diagnostyka=diagnostyka,
        cel_testu=cel_testu
    )

    st.write(response)
