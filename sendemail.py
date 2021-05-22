import smtplib,yaml
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
with open("data.yaml") as stream:
    data_loaded = yaml.safe_load(stream)
 
def sendingemail():
    #print("Inside sending email")
    email_to=[]
    Cc=data_loaded['Cc'].split(',')
    for k in Cc:
        email_to.append(k)
    To=data_loaded['To'].split(',')
    for k in To:
        email_to.append(k)
        
    body1 ='''
            <p>&nbsp;</p>
            <h3>{b1}</h3>
            <h3>{b2}</h3>
            <h3>{b3}</h3>
              <p>&nbsp;</p>
           '''
    body1=body1.format(b1=data_loaded['Mail_Body1'],
    b2=data_loaded['Mail_Body2'], 
    b3=data_loaded['Mail_Body3']+":")
        

        #print("Email body")
    msg = MIMEMultipart('alternative')
    if data_loaded['Email_Attachment_path']!='None':
        with open(data_loaded['Email_Attachment_path'], 'rb') as at:
            mime = MIMEBase('file', 'msg', filename=data_loaded['Attahment_name'])
                # add required header data:
            mime.add_header('Content-Disposition', 'attachment', filename=data_loaded['Attahment_name'])
            mime.add_header('X-Attachment-Id', '0')
            mime.add_header('Content-ID', '<0>')
                # read attachment file content into the MIMEBase object
            mime.set_payload(at.read())
                # encode with base64
            encoders.encode_base64(mime)
                # add MIMEBase object to MIMEMultipart object
            msg.attach(mime)

    email_subject = data_loaded['Subject']
    email_from = data_loaded['From']
        #email_to = data_loaded['To']
    email_cc = data_loaded['Cc']
    msg['To'] = ", ".join(email_to)
    msg['CC'] = email_cc
    msg['Subject'] = email_subject
        
    mt_html = MIMEText(body1, 'html')
    msg.attach(mt_html)
    try:
        smtpObj = smtplib.SMTP(data_loaded['SMTP_SERVER'])
        smtpObj.sendmail(email_from, email_to, msg.as_string())  
        print("Email Sent Successfully") 
    except:
        print("Error:unable to send email \n")
    smtpObj.quit()
sendingemail()