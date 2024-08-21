from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Consultant
import pandas as pd
from . import sending_mail

# Load the Excel file
df = pd.read_excel(r'datasetadr')

# Clear existing consultants from the database
Consultant.objects.all().delete()

def display_excel(request):
    consultant_set = set()

    # Check if there are any consultants in the database
    if Consultant.objects.count() == 0:
        for i in range(len(df)):
            consultant_name = df.iloc[i, 3]
            consultant_mail = df.iloc[i, 4]

            if consultant_name not in consultant_set:
                Consultant.objects.create(name=consultant_name, mail=consultant_mail)
                consultant_set.add(consultant_name)

    tabloBaslik = "<table style='width:100%' border='1px solid black'>"
    tabloBaslik += "<tr><th></th><th>Tür</th><th>Öğrenci No-1</th><th>Öğrenci No-2</th><th>Danışman</th><th>Danışman Mail</th><th>Asistan</th><th>Asistan Mail</th> <th>Proje Adı</th></tr>"
    
    for i in range(len(df)):
        yardimci = df.iloc[i, 5]
        danisman = df.iloc[i, 3]
        ogrNo1 = df.iloc[i, 1]
        ogrNo2 = df.iloc[i, 2]
        tur = df.iloc[i, 0]
        yardimciMail = df.iloc[i, 6]
        danismanMail = df.iloc[i, 4]
        projeAd = df.iloc[i , 7]
        #consultant_id = Consultant.objects.filter(name=danisman).values_list('id', flat=True).first()
        
        tabloBaslik += f"<tr><th><a href='#' id='{i}' onclick='sendToOne({i})'>Send</a></th><th>{str(tur)}</th><th>{str(ogrNo1)}</th><th>{str(ogrNo2)}</th><th>{str(danisman)}</th><th>{str(danismanMail)}</th><th>{str(yardimci)}</th><th>{str(yardimciMail)}</th><th>{str(projeAd)}</th></tr>"

    tabloBaslik += "</table>"

    consultants = Consultant.objects.all().values_list('id', 'name').distinct()
    consultants_list = list(consultants)

    return render(request, 'display_excel.html', {'html_table': tabloBaslik, 'consultants': consultants_list})

def send_to_one(request, id):
    note_type = request.GET.get('noteType')
    print(str(note_type))
    yardimci = df.iloc[id, 5]
    danisman = df.iloc[id, 3]
    ogrNo1 = df.iloc[id, 1]
    ogrNo2 = df.iloc[id, 2]
    tur = df.iloc[id, 0]
    yardimciMail = df.iloc[id, 6]
    danismanMail = df.iloc[id, 4]
    projeAd = df.iloc[id, 7]
    araLink = df.iloc[id, 8] 
    finalLink = df.iloc[id, 9]
    butLink = df.iloc[id, 10]
    
    text = "<br> NOT: Proje danışmanları içerik ve şekil yönünden, proje yardımcıları sadece şekil yönünden raporları kontrol edecektir. "
    text += "<br> <br> Kolaylıklar dileriz. <br> <br> Proje Koordinatörlüğü <br> <br> "
    tabloBaslik = "<table style=\"width:100%\" border=\"1px solid black\">"
    tabloBaslik += " <tr> <th>Tür</th> <th>Öğrenci No-1</th> <th>Öğrenci No-2</th>  <th>Danışman</th>  <th>Asistan</th> <th>Asistan Mail</th> <th>Proje Adı</th> "
    if(str(note_type) == "Ara Rapor"):
        tabloBaslik += "<th>Ara Rapor Linki</th> </tr> "
        text += tabloBaslik
        tabloIcerik = ""
        tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{str(danisman)}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(araLink)}</td></tr>"

    elif(str(note_type) == "Final"):
        tabloBaslik += "<th>Final Linki</th> </tr> "
        text += tabloBaslik
        tabloIcerik = ""
        tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{str(danisman)}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(finalLink)}</td></tr>"

    else:
        tabloBaslik += "<th>Bütünleme Linki</th> </tr> "
        text += tabloBaslik
        tabloIcerik = ""
        tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{str(danisman)}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(butLink)}</td></tr>"

   
    tmp = text + tabloIcerik + "</table>"
    sending_mail.send_to_consultant(str(danismanMail), tmp)
    messages.success(request, 'Mail Sent!')
    return redirect('display_excel')


def send_to_all_consultant(request):
    note_type = request.GET.get('noteType')
    text = "<br> NOT: Proje danışmanları içerik ve şekil yönünden, proje yardımcıları sadece şekil yönünden raporları kontrol edecektir. "
    text += "<br> <br> Kolaylıklar dileriz. <br> <br> Proje Koordinatörlüğü <br> <br> "
    tabloBaslik = "<table style=\"width:100%\" border=\"1px solid black\">"
    tabloBaslik += " <tr> <th>Tür</th> <th>Öğrenci No-1</th> <th>Öğrenci No-2</th>  <th>Danışman</th>  <th>Asistan</th> <th>Asistan Mail</th> <th>Proje Adı</th> "
    if(str(note_type) == "Ara Rapor"):
        tabloBaslik += "<th>Ara Rapor Linki</th> </tr> "
    elif(str(note_type) == "Final"):
        tabloBaslik += "<th>Final Linki</th> </tr> "
    else:
        tabloBaslik += "<th>Bütünleme Linki</th> </tr> "

    text += tabloBaslik
    tabloIcerik = ""

    danismanEski = df.iloc[0, 3]
    for i in range(len(df)):
        danismanYeni = df.iloc[i, 3]  
        if str(danismanYeni) != str(danismanEski):
            danismanEski = danismanYeni 
            #MAIL
            tmp = text + tabloIcerik + "</table>"
            sending_mail.send_to_consultant(str(danismanMail), tmp)
            # Reset the content table for the new consultant
            tabloIcerik = ""

        yardimci = df.iloc[i, 5]  
        ogrNo1 = df.iloc[i, 1]
        ogrNo2 = df.iloc[i, 2]    
        tur = df.iloc[i, 0]  
        yardimciMail = df.iloc[i, 6]    
        danismanMail = df.iloc[i, 4]
        projeAd = df.iloc[i, 7]
        araLink = df.iloc[i, 8] 
        finalLink = df.iloc[i, 9]
        butLink = df.iloc[i, 10]
        if(str(note_type) == "Ara Rapor"):
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{str(danismanYeni)}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(araLink)}</td></tr>"
        elif(str(note_type) == "Final"):
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{str(danismanYeni)}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(finalLink)}</td></tr>"
        else:
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{str(danismanYeni)}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(butLink)}</td></tr>"
        

    tmp = text + tabloIcerik + "</table>"
    sending_mail.send_to_consultant(str(danismanMail), tmp)
    return render(request, 'sent_all_consultant.html', {'tip' : str(note_type)})


def send_to_consultant(request, consultant_id ):
    note_type = request.GET.get('noteType')
    print(str(note_type))
    consultant = get_object_or_404(Consultant, id=consultant_id)
    print(f"Consultant ID: {consultant.id}, Name: {consultant.name}")
    text = "<br> NOT: Proje danışmanları içerik ve şekil yönünden, proje yardımcıları sadece şekil yönünden raporları kontrol edecektir. "
    text += "<br> <br> Kolaylıklar dileriz. <br> <br> Proje Koordinatörlüğü <br> <br> "
    tabloBaslik = "<table style=\"width:100%\" border=\"1px solid black\">"
    tabloBaslik += " <tr> <th>Tür</th> <th>Öğrenci No-1</th> <th>Öğrenci No-2</th>  <th>Danışman</th>  <th>Asistan</th> <th>Asistan Mail</th> <th>Proje Adı</th> "
    if(str(note_type) == "Ara Rapor"):
        tabloBaslik += "<th>Ara Rapor Linki</th> </tr> "
    elif(str(note_type) == "Final"):
        tabloBaslik += "<th>Final Linki</th> </tr> "
    else:
        tabloBaslik += "<th>Bütünleme Linki</th> </tr> "

    text += tabloBaslik
    tabloIcerik = ""

    # Find the starting index for the selected consultant
    i = 0
    while i < len(df) and str(df.iloc[i, 3]) != consultant.name:
        i += 1

    # Check if the consultant was found and handle the case where the index is out of bounds
    if i >= len(df) or str(df.iloc[i, 3]) != consultant.name:
        return render(request, 'error.html', {'message': 'Consultant not found in data.'})

    # Collect data for the selected consultant
    while i < len(df) and str(df.iloc[i, 3]) == consultant.name:
        yardimci = df.iloc[i, 5]  
        ogrNo1 = df.iloc[i, 1]
        ogrNo2 = df.iloc[i, 2]    
        tur = df.iloc[i, 0]  
        yardimciMail = df.iloc[i, 6]    
        danismanMail = df.iloc[i, 4]
        projeAd = df.iloc[i, 7]
        araLink = df.iloc[i, 8] 
        finalLink = df.iloc[i, 9]
        butLink = df.iloc[i, 10]
        if(str(note_type) == "Ara Rapor"):
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{consultant.name}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(araLink)}</td></tr>"
        elif(str(note_type) == "Final"):
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{consultant.name}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(finalLink)}</td></tr>"
        else:
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{consultant.name}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(butLink)}</td></tr>"
        i += 1

    tmp = text + tabloIcerik + "</table>"
    sending_mail.send_to_consultant(consultant.mail, tmp)

    return render(request, 'sent_to_consultant.html', {'consultant': consultant})


def send_to_consultant_and_assistant(request, consultant_id):
    note_type = request.GET.get('noteType')
    print(str(note_type))
    consultant = get_object_or_404(Consultant, id=consultant_id)
    # Prepare the email content
    text = "<br>NOT: Proje danışmanları içerik ve şekil yönünden, proje yardımcıları sadece şekil yönünden raporları kontrol edecektir.<br><br>Kolaylıklar dileriz.<br><br>Proje Koordinatörlüğü<br><br>"
    tabloBaslik = "<table style=\"width:100%\" border=\"1px solid black\">"
    tabloBaslik += " <tr> <th>Tür</th> <th>Öğrenci No-1</th> <th>Öğrenci No-2</th>  <th>Danışman</th>  <th>Asistan</th> <th>Asistan Mail</th> <th>Proje Adı</th> "
    if(str(note_type) == "Ara Rapor"):
        tabloBaslik += "<th>Ara Rapor Linki</th> </tr> "
    elif(str(note_type) == "Final"):
        tabloBaslik += "<th>Final Linki</th> </tr> "
    else:
        tabloBaslik += "<th>Bütünleme Linki</th> </tr> "

    text += tabloBaslik
    tabloIcerik = ""
    yardimciMailList = []
    i = 0

    while i < len(df) and str(df.iloc[i, 3]) != consultant.name:
        i += 1

    while i < len(df) and str(df.iloc[i, 3]) == consultant.name:
        yardimci = df.iloc[i, 5]
        ogrNo1 = df.iloc[i, 1]
        ogrNo2 = df.iloc[i, 2]
        tur = df.iloc[i, 0]
        yardimciMail = df.iloc[i, 6]
        projeAd = df.iloc[i, 7]
        araLink = df.iloc[i, 8] 
        finalLink = df.iloc[i, 9]
        butLink = df.iloc[i, 10]
        if yardimciMail not in yardimciMailList:
            yardimciMailList.append(str(yardimciMail))

        if(str(note_type) == "Ara Rapor"):
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{consultant.name}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(araLink)}</td></tr>"
        elif(str(note_type) == "Final"):
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{consultant.name}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(finalLink)}</td></tr>"
        else:
            tabloIcerik += f"<tr> <td>{str(tur)}</td> <td>{str(ogrNo1)}</td> <td>{str(ogrNo2)}</td>  <td>{consultant.name}</td> <td>{str(yardimci)}</td><td>{str(yardimciMail)}</td><td>{str(projeAd)}</td><td>{str(butLink)}</td></tr>"
        
        i += 1

    tmp = text + tabloIcerik + "</table>"
    
    # Print for debugging
    print(f"Consultant: {consultant.name}")
    print(f"Tablo Icerik: {tabloIcerik}")
    print(f"Yardimci Mail List: {yardimciMailList}")

    sending_mail.send_to_consultant_and_assistant(consultant.mail, yardimciMailList, tmp)

    return render(request, 'sent_to_consultant.html', {'consultant': consultant})

