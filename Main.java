package polymorphism;
import java.io.*;
import java.util.Iterator;
import java.util.Map;
import java.util.TreeMap;

///// Written by Hank Davis
///// Summer 2020
///// "Yeet and Retreat" - Nate

///// I used Apache POI to access, read, and write to the Excel files
///// Here is GFG documentation: https://www.geeksforgeeks.org/reading-writing-data-excel-file-using-apache-poi/?ref=rp
///// General link to the resource: https://poi.apache.org/
///// I may have used this: https://howtodoinjava.com/java/library/readingwriting-excel-files-in-java-poi-tutorial/#writing_excel_file

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class Main {

    // the file we're going to write to once we have made our decision based on the input!
    ////////////////// You'll need to change the file paths to match the path on your machine.
    private static final String FILE_NAME = "/Users/Hank Davis/Downloads/Startup EE364E/FinalizedSendersList.xlsx";

    public static void main(String[] args)  {

        try{
//            System.out.println("Yo Yo Yo it's Skinny Pete");  // it's from breaking bad if you're out of the loop
            ////////////////// You'll need to change the file paths to match the path on your machine.
            FileInputStream fisResidences = new FileInputStream(new File("/Users/Hank Davis/Downloads/Startup EE364E/Example Data for ResidencesV2.xlsx"));
            FileInputStream fisSenders = new FileInputStream(new File("/Users/Hank Davis/Downloads/Startup EE364E/Example Data for SendersV2.xlsx"));

            XSSFWorkbook wbResi = new XSSFWorkbook(fisResidences);
            XSSFWorkbook wbSender = new XSSFWorkbook(fisSenders);

            XSSFSheet sheetResi = wbResi.getSheetAt(0);     //creating a Sheet object to retrieve object
            XSSFSheet sheetSender = wbSender.getSheetAt(0);     //creating a Sheet object to retrieve object

            ////// creating the Excel file for the FINAlIZED Sender's list, to be used after running through the program.
            ///// I do not know where the new EXCEL file is supposed to be in the file structure once the program has run.
            // Blank workbook
            XSSFWorkbook wbNewSenderList = new XSSFWorkbook();
            // Create a blank sheet
            XSSFSheet sheetNewSenderList = wbNewSenderList.createSheet("Revised Sender's List");
            // This data needs to be written (Object[])
            Map<Integer, Object[]> dataForNewSheet = new TreeMap<>();

            //// apparently these weren't used/referrenced. I'm scared to delete em tho.
            Iterator<Row> rowIteratorResi = sheetResi.iterator();
            Iterator<Row> rowIteratorSender = sheetSender.iterator();

            System.out.println("Physical number of rows, Resi: " + sheetResi.getPhysicalNumberOfRows());
            System.out.println("Physical number of rows, Sender: " + sheetSender.getPhysicalNumberOfRows());
            System.out.println("Last row number of rows, Resi: " + sheetResi.getLastRowNum());
            System.out.println("Last row number of rows, Sender: " + sheetSender.getLastRowNum());

            //while (rowIteratorSender.hasNext()) {
            // goes through all of the rows, there are 20 entries, 21 total rows

            Row rowSender = sheetSender.getRow(0);
            Cell cellSender;

            Row rowResi = sheetResi.getRow(0);
            Cell cellResi;

            // Excel spreadsheets start counting at 1.
            int counterForRevisedEntries = 1;

            //// setting the column headers:
            Row rowFinalizedSetting = sheetNewSenderList.createRow(0);
            int cellNumberSetting = 0;
            for(int p = 0; p < 8 ; p++){
                // the cell where we want to write the data
                Cell cellFinalized = rowFinalizedSetting.createCell(cellNumberSetting++);
                /// gets the first row, the column headers
                cellFinalized.setCellValue(sheetResi.getRow(0).getCell(p).toString());
            }

            for(int senderCurrRow = 0; senderCurrRow < 21; senderCurrRow++){
                rowSender = sheetSender.getRow(senderCurrRow);
                // For each row, iterate through all the columns
                // goes through each cell (there are 8 collumns total)

                //// Next 5 lines is probably all trash, aka it can be deleted.
//
//                for(int senderCurrCol = 0; senderCurrCol < 7; senderCurrCol++){
//                    cellSender = rowSender.getCell(senderCurrCol);
//                    valueSenderCell = cellSender.getStringCellValue();
//                    System.out.println(" ******************* SENDER, In the cell: " + cellSender);
                //// End of the probably trash code zone.

                    ///// currently a fixed number of Rows. This will need to be changed as the rows is a variable of course.
                    for(int resiCurrRow = 0; resiCurrRow < 21; resiCurrRow++){
                        rowResi = sheetResi.getRow(resiCurrRow);

                            //// does the first name match ?
                            if(rowSender.getCell(0).toString().equals(rowResi.getCell(0).toString())){
                                System.out.println("0th one matched!");

                                ////// does the first name match ?
                                if(rowSender.getCell(1).toString().equals(rowResi.getCell(1).toString())){
                                    System.out.println("1st one matched!");

                                    /////// does the phone number match ?
                                    if(rowSender.getCell(2).toString().equals(rowResi.getCell(2).toString())){
                                        System.out.println("\t2nd one matched!");

                                        ///// if the last three have matched and we are here now, we know we have the right person
                                        ///// so if something about thier address data does not match up, then they have moved. The address in the
                                        ///// sender's address list is incorrect and needs to be updated
                                        //// does the address match?
                                        if(rowSender.getCell(3).toString().equals(rowResi.getCell(3).toString())){
                                            System.out.println("\t\t3rd one matched!");
                                            //// does the apartment number (if applicable) match??

                                            if(rowSender.getCell(4).toString().equals(rowResi.getCell(4).toString())){
                                                System.out.println("\t\t\t4th one matched!");

                                                //// Does the city match ?
                                                if(rowSender.getCell(5).toString().equals(rowResi.getCell(5).toString())){
                                                    System.out.println("\t\t\t\t5th one matched!");

                                                    //// Does the state match?
                                                    if(rowSender.getCell(6).toString().equals(rowResi.getCell(6).toString())){
                                                        System.out.println("\t\t\t\t\t6th one matched!");

                                                        // does the zip code match?
                                                        if(rowSender.getCell(7).toString().equals(rowResi.getCell(7).toString())){
                                                            System.out.println("\t\t\t\t\t\t7th one matched!");
                                                                System.out.println("**^*^*^WE GOT US A TOTAL MATCH HERE*^*^*");
                                                                System.out.println("Sender side addressee: " + rowSender.getCell(1).toString() + " " + rowSender.getCell(0).toString()
                                                                        + " And Resident is: " + rowResi.getCell(1).toString() + " " + rowResi.getCell(0).toString());
                                                            //// we should add this entry in the sender's list to the FINALIZED sender's list
                                                            ///// I do not know where the new EXCEL file is supposed to be or where it should go.
                                                            Row rowFinalized = sheetNewSenderList.createRow(counterForRevisedEntries);
                                                            int cellNumber = 0;
                                                            for(int p = 0; p < 8 ; p++){
                                                                // the cell where we want to write the data
                                                                Cell cellFinalized = rowFinalized.createCell(cellNumber++);
                                                                cellFinalized.setCellValue(rowResi.getCell(p).toString());
                                                            }
//                                                            dataForNewSheet.put(rowFinalized, new Object[]{ rowResi } );
                                                            counterForRevisedEntries++; // we had a successfull add so add one more
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        ///// have an else statement here. If the address does not match, then insert the updated one into the sender's FINALIZED List
                                        else{
                                            System.out.println("This is where the address is updated in the sender's list. Sender had the same person, but old address");
                                        }
                                    }
                                    ///// have an else statement here in case they changed their phone number but the address info is all the same
                                }
                            }
    //                    }
                    }
//                }
                System.out.println("");
            }

            try {
                FileOutputStream outputStream = new FileOutputStream(FILE_NAME);
                wbNewSenderList.write(outputStream);
                wbNewSenderList.close();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            fisResidences.close();           //// needs to be for both the Resi and Sender sheets !!!!
            fisSenders.close();           //// needs to be for both the Resi and Sender sheets !!!!
        }

        catch(Exception e) {
            e.printStackTrace();
        }
    }
}
