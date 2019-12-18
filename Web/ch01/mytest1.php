<?php
   if (isset($_POST['action'])) {
      echo "Hello world from PHP";

      $z_name = $_POST["z_name"] ;
      $z_price = $_POST["z_price"] ;
      $z_descr = $_POST["z_descr"] ;

      $servername = "localhost";
      $username = "root";
      $password = "";
      $dbname = "test";

      // Create connection
      $conn = new mysqli($servername, $username, $password, $dbname);

      // Check connection
      if ($conn->connect_error) {
         die ("Connection failed: " . $conn->connect_error);
      }
      
      echo "<br> Connected successfully";

      $sqlInsert = $conn->prepare("insert into Products values (?, ?, ?)");
      $sqlInsert->bind_param("sds", $z_name, $z_price, $z_descr);
      if ($sqlInsert->execute() === TRUE) {
         // echo "New record created successfully";
      } else {
         echo "Error: " . $sqlInsert . "<br>" . $conn->error;
      }


      $sqlInsert->close();
      $conn->close(); 
   }

?>
   

