from flask import Flask,request,jsonify
from flask_cors import CORS
import yagmail
import ast
from smtplib import SMTP

mail_id = "conference@aipatasala.com"
mail_password = "Aip@2021"
mail_host = 'smtp.gmail.com'
mail_port = 587


# mail_host = "webmail.mahantecth.com"
# mail_port = "995"
# mail_id = "s2t@mahantech.com"
# mail_password = "Minds2Machines"

aipatasala_smtp = yagmail.SMTP(mail_id,mail_password)

#
# smtp = SMTP(mail_host, mail_port)
# smtp.starttls()
# # Authentication
# smtp.login(mail_id, mail_password)
#
# send_mail_id = "kunduruanilwork@gmail.com"
# message = "hello"
# smtp.sendmail(mail_id, send_mail_id, message)

application = Flask(__name__)
CORS(application)

send_mail_body = """inviting you to a scheduled  meeting.

Topic: {topic}
Time: {time}

Join Meeting
{URL}

Password for login : {password}

Meeting ID: {meeting_id}


"""

cancel_mail_body = """inviting you to a scheduled  meeting has cancelled due to {reason}.

Topic: {topic}
Time: {time}

Join Meeting
{URL}

Password for login : {password}

Meeting ID: {meeting_id}


"""

@application.route('/')
def hello_world():
    return "hello world S2T send mail !!!"

@application.route('/s2t/cancelinvite', methods = ['POST'])
def cancel_send_mail():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            subject = "RE:Meeting Invitation For meeting ID : {} ".format(str(data["meeting_id"]))
            for senders in data["users"]:
                mail = senders["email"]
                password = senders["password"]
                body = cancel_mail_body.format_map({"reason":data["reason"],"topic":data["topic"],"time":data["time"],"URL":data["URL"],
                                        "meeting_id":str(data["meeting_id"]),"password":password})
                aipatasala_smtp.send(to=mail,subject=subject,contents=body)
            return jsonify({"msg":"sent"}),200
        else:
            return jsonify({"msg":"Bad request"}),400
    except Exception as e:
        print(str(e))
        return jsonify({"msg":"Internal Server Error"}),500


@application.route('/s2t/sendmail', methods = ['POST'])
def user_send_mail():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            subject = "Meeting Invitation For meeting ID : {} ".format(str(data["meeting_id"]))
            for senders in data["users"]:
                mail = senders["email"]
                password = senders["password"]
                body = send_mail_body.format_map({"topic":data["topic"],"time":data["time"],"URL":data["URL"],
                                        "meeting_id":str(data["meeting_id"]),"password":password})
                aipatasala_smtp.send(to=mail,subject=subject,contents=body)
            return jsonify({"msg":"sent"}),200
        else:
            return jsonify({"msg":"Bad request"}),400
    except Exception as e:
        print(str(e))
        return jsonify({"msg":"Internal Server Error"}),500


if __name__ == '__main__':
    application.run(host='0.0.0.0',  debug=True)