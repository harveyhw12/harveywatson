import java.net.*;
import java.io.*;

import java.time.format.DateTimeFormatter;
import java.time.LocalDateTime;

public class ClientHandler extends Thread {
    //client handler class extends thread in order to give each user a new thread and allow concurrent access
    //instantiates the socket to connect the client to
    private Socket socket = null;   

    public ClientHandler(Socket socket) {
        super("ClientHandler");
        this.socket = socket;
    }

    //run() will handle the data recieved from the client
    public void run() {
        //initialised all of the local variables needed for run
        DataOutputStream out = null;
        BufferedReader in = null;
        String[] arguments = null;
        String command = null;
        String filename = null;
        int num_args = 0;

        try {
            //attempts to retrieve the streams from the socket
            out = new DataOutputStream(socket.getOutputStream());
            in = new BufferedReader(new InputStreamReader((socket.getInputStream())));
        } catch (IOException e) {
            System.err.println("Error retrieveing I/O streams from socket");
            try{
                socket.close();
            } catch (IOException w) {
                System.err.println("Error closing the socket to the client");
            }        
        }
        try {
            //reads the command sent by the client
            String temp = in.readLine();
            num_args = Integer.parseInt(temp);
            arguments = new String[num_args];
            for (int i = 0; i < num_args; i++) {
                arguments[i] = in.readLine();
            }
            command = arguments[0];
            System.out.print("Recieved:");
            for (int i = 0; i < arguments.length; i++) {
                System.out.print(" " + arguments[i]);
            }
            System.out.print('\n');
        } catch (IOException e) {
            System.err.println("Command sent by the client not recieved");
            try{
                socket.close();
            } catch (IOException a) {
                System.err.println("Error closing the socket to the client");
            }        
        }
        //gathers the information needed to log the clients request
        InetAddress inet = socket.getInetAddress();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyy:HH:mm:ss");
        LocalDateTime time = LocalDateTime.now();
        File log = null;
        log = new File("log.txt");
        //creates a new log when the server starts

        try {
            //opens the log file and writes all the corresponding data
            FileWriter toLog = new FileWriter(log, true);
            toLog.write(formatter.format(time)+':');
            toLog.write(inet.getHostAddress()+ ':');
            for (int i = 0; i < arguments.length; i++) {
                toLog.write(arguments[i]);
                if (i != arguments.length-1) {
                    toLog.write(" ");
                }
            }
            toLog.write('\n');
            toLog.close();
        } catch (IOException e) {
            System.err.println("Error writing to the log file");
            try{
                socket.close();
            } catch (IOException l) {
                System.err.println("Error closing the socket to the client");
            }       
        }
        // System.out.println(command);
        if (!command.equals("list") && !command.equals("get")) {
            try {
                out.writeBoolean(false);
            } catch (IOException e) {
                try {
                    System.err.println("Error returning success status");
                    socket.close();
                } catch (IOException q) {
                    System.err.println("Error closing the socket to the client");
                }
            }
        } else if (arguments.length > 1 && command.equals("list")) {
            try {
                socket.close();
            } catch (IOException e) {
                System.err.println("Too many arguments received for list");
            }
        } else {
            try {
                out.writeBoolean(true);
            } catch (IOException e) {
                System.err.println("Error closing the socket to the client");
            }
        }
    //creates a new fileprotocol to handle the client's requests
    FileProtocol p = new FileProtocol();
    // if the command equals list
    if (command.equals("list") && arguments.length == 1) {

        //retrieves the list of files in the serverfiles directory
        String[] files = p.handleList();
        //echoes the file list to the server
        for (int i = 0; i < files.length; i++) {
            System.out.println(files[i]);
        }
        try {
            //writes the number of files to the client
            out.write(files.length);
        } catch (IOException e) {
            System.err.println("Error writing the number of files to the client");
            try{
                socket.close();
            } catch (IOException r) {
                System.err.println("Error closing the socket to the client");
            }
        }
        //joins the list of files with a semicolon since they cannot be in filenames and convert to bytes
        byte[] to_send = String.join(":", files).getBytes();
        try {
            //writes the list of files to the client's stream
            out.write(to_send);
        } catch (IOException e) {
            System.err.println("Error sending the list of files to the client");
            try{
                socket.close();
            } catch (IOException g) {
                System.err.println("Error closing the socket to the client");
            }
        }   
    } else if (command.contains("get")) {
        //if command equals get
        filename = arguments[1];
        //sends the filename to handleget which will return a byte[] array of the requested file
        byte[] toSend = p.handleGet(filename);
        if (toSend == null) {
            System.err.println("File could not be found");
            // System.exit(-1);
            try{
                socket.close();
            } catch (IOException e) {
                System.err.println("Error closing the socket to the client");
            }
        }
        try {
            //sends the file length to the client
            out.writeInt(toSend.length);
        } catch (IOException e) {
            System.err.println("Error writing file size to the client");
            try{
                socket.close();
            } catch (IOException a) {
                System.err.println("Error closing the socket to the client");
            }
        }
        try {   
            //writes the actual byte array to the client which is now ready to recieve it
            out.write(toSend, 0, toSend.length);
        } catch (IOException e) {
            System.err.println("Error writing the requested file to the client");
            try{
                socket.close();
            } catch (IOException n) {
                System.err.println("Error closing the socket to the client");
            }
        }
    }
        try{    
            //closes all of the streams
            out.close();
            in.close();
            socket.close();
        } catch (IOException e) {
            System.err.println("Error closing streams or socket");
            System.exit(-1);
        }
    }
}
