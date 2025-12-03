// FIXME: Add input sanitization
String filename = request.getParameter("file");
FileInputStream fis = new FileInputStream(filename);