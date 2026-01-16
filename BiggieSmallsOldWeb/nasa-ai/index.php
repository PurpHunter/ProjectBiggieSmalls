<?php include 'DynamicWebFiles\header.php' ?>

<script>
document.title = "Astralis | Home Page";
</script>

<div style="position: absolute; top: 10px; right: 10px; font-size: 20px;">
  <i>Welcome, <?php echo htmlspecialchars($username); ?>!</i>
</div>

<h1>Home Page</h1>

<?php include 'DynamicWebFiles\sidebar.php' ?>

<?php include 'DynamicWebFiles\aiScripts.php'; ?>

</body>
</html>

