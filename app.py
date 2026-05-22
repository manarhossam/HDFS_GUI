from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', output='')

@app.route('/run', methods=['POST'])
def run():
    command_type = request.form['command']
    path1 = request.form.get('path1', '').strip()
    path2 = request.form.get('path2', '').strip()

    cmd = ""

    if command_type == "ls":
        cmd = f"hdfs dfs -ls {path1}"

    elif command_type == "mkdir":
        cmd = f"hdfs dfs -mkdir {path1}"

    elif command_type == "rm":
        cmd = f"hdfs dfs -rm {path1}"

    elif command_type == "put":
        cmd = f"hdfs dfs -put {path1} {path2}"

    elif command_type == "get":
        cmd = f"hdfs dfs -get {path1} {path2}"

    elif command_type == "cp":
        cmd = f"hdfs dfs -cp {path1} {path2}"

    elif command_type == "mv":
        cmd = f"hdfs dfs -mv {path1} {path2}"

    elif command_type == "cat":
        cmd = f"hdfs dfs -cat {path1}"

    elif command_type == "jps":
        cmd = "jps"

    if not cmd:
        output = "Unknown command."

    else:
        try:
            full_cmd = f"source ~/.bashrc && {cmd}"

            result = subprocess.run(
                full_cmd,
                shell=True,
                executable="/bin/bash",
                capture_output=True,
                text=True
            )

            output = result.stdout + result.stderr

        except Exception as e:
            output = str(e)

    return render_template("index.html", output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
