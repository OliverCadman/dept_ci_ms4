
  // Format date to remove Python's TZ info in datetime object
  // and make it readable for the user.
  // https://stackoverflow.com/questions/25275696/javascript-format-date-time
  function formatDate(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    hours = hours % 24;
    hours = hours ? hours : 24;
    minutes = minutes < 10 ? "0" + minutes : minutes;

    let strTime = hours + ":" + minutes;
    return (
      date.getDate() +
      1 +
      "/" +
      (date.getMonth() + 1) +
      "/" +
      date.getFullYear() +
      " " +
      strTime
    );
  }

  // Calculate the difference between two dates (UTC Aware)
  // https://stackoverflow.com/questions/3224834/get-difference-between-2-dates-in-javascript
  const _MS_PER_DAY = 1000 * 60 * 60 * 24;

  function dateDiffInDays(a, b) {
    // Discard the time and time-zone information.
    const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
    const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

    return Math.floor((utc2 - utc1) / _MS_PER_DAY);
  }
