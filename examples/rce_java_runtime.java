// Java Runtime.exec() RCE
import java.io.*;

public class FileProcessor {
    public void processFile(String filename) throws IOException {
        // VULNERABLE: Command injection
        Runtime.getRuntime().exec("cat " + filename);
    }
}
