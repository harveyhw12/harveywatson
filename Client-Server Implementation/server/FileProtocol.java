import java.net.*;
import java.io.*;
import java.io.File;

public class FileProtocol {
    //fileprotocol class handles the requests by the clients

    public String[] handleList() {
        //when the client requests list, this function returns a string of filenames to return
        File dir = new File("./serverFiles");
        String[] list = dir.list();
        return list;
    }

    public byte[] handleGet(String file) {
        //this function runs when the clients requests get fname
        //it begins by initialising the method's variables
        File to_send = null;
        FileInputStream read_file = null;
        byte[] as_bytes = null;

        //tries to open the file requested by the user
        try {
            to_send = new File("./serverFiles/"+file);
            //creates a new FileInputStream to read the file and reads it into bytes
            read_file = new FileInputStream(to_send);
            //creates a byte[] array to read the file into, the size of the file casted to an integer
            as_bytes = new byte[(int) to_send.length()];
            //reads the file into the byte[] array and closes it
            read_file.read(as_bytes);
            read_file.close();
        } catch(FileNotFoundException e) {
            //throws FileNotFoundException if the requested file does not exist
            // System.out.println("File could not be found");
            // System.exit(-1);
            return null;
        } catch(IOException e) {
            //If at any point of execution an IO exception occurs, catches the error
            System.out.println("IOException has occurred in the FileProtocol");
            // System.exit(-1);
            return null;
        }
        return as_bytes;
    }
}
