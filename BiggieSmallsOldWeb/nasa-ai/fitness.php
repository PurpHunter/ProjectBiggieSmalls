<?php include 'DynamicWebFiles\header.php' ?>

<style> body { background-color: #99d7f0ff; } </style>

<script>
document.title = "Astralis | Fitness Page";
</script>

<div style="position: absolute; top: 10px; right: 10px; font-size: 20px;"> <!-- Username top right of the screen. -->
  <i>Welcome, <?php echo $username;?>!</i>
</div>

<h1>Fitness Page</h1><!-- Says the page currently on. -->

<?php include 'DynamicWebFiles\sidebar.php' ?>

<?php include 'DynamicWebFiles\aiScripts.php'; ?>

</body>
</html>
