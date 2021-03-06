let pieces = document.getElementById("pieces");
let segments = document.getElementById("segments");
let colors = document.getElementById("colors");
let amount = document.getElementById("amount");
let generate_rand = document.getElementById("generate_random");
let start_index = document.getElementById("start");
let stop_index = document.getElementById("stop");
let generate_range = document.getElementById("generate_range");
let circle_index = document.getElementById("circle_index");
let generate_single = document.getElementById("generate_single");
let error = document.getElementById("error");
let comment = document.getElementById("comment");
let svg_area = document.getElementById("svg_area");

// Multiplies together [start, end] as a BigInt
function multiply_range(start, end) {
  let res = 1n;
  for (let i = start; i <= end; i++) {
    res *= i;
  }
  return res;
}

function factorial(n) {
  return multiply_range(1n, n);
}

// min function that works with BigInt
function min(a, b) {
  if (a < b) {
    return a;
  } else {
    return b;
  }
}

// n*(n-1)*....*(n-r+1)
function permutations(n, r) {
  return multiply_range(n - r + 1n, n);
}

// n*(n-1)*....*(n-r+1) / factorial(r)
function combinations(n, r) {
  r = min(r, n - r); // performance increase
  numer = multiply_range(n - r + 1n, n);
  denom = multiply_range(1n, r);
  return numer / denom;
}

function extract_digits(n, bases) {
  // Turns a number into a set of digits given a list of bases
  let digits = [];
  for (const base of bases) {
    let digit = n % base;
    n = n / base;

    digits.push(digit);
  }
  return digits;
}

// https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)
function star_bars_count(s, b) {
  // Determines the number of permutations for this star and bar configuration
  return combinations(s + b, b);
}

function star_bars_unrank(rank, stars, bars, groups = [0]) {
  /*
    Determine the group counts associated with the rank
    for a given star and bar configuration.
    Based off of perm_unrank from https://codegolf.stackexchange.com/a/115024

    It works by building up the star and bar permutation by choosing either
    a star or a bar to add. We remove the string representation of the
    permutation here and just store the group counts that correspond to the
    particular star and bar arrangement.
    i.e. **||*| = [2, 0, 1, 0]
    */

  // Return if we only have one choice left
  if (stars == 0n || bars == 0n) {
    while (bars > 0n) {
      groups.push(0);
      bars -= 1n;
    }
    while (stars > 0n) {
      groups[groups.length - 1] += 1;
      stars -= 1n;
    }

    return groups;
  }

  // Possible arrangements if we remove 1 star
  let star_count = star_bars_count(stars - 1n, bars);

  // We're adding a star, so the last group increments
  if (star_count > rank) {
    groups[groups.length - 1] += 1;
    return star_bars_unrank(rank, stars - 1n, bars, groups);
  }

  // Possible arrangements if we remove 1 bar
  let bar_count = star_bars_count(stars, bars - 1n);

  // We're adding a bar, so we're adding a new group
  if (star_count + bar_count > rank) {
    groups.push(0);
    return star_bars_unrank(rank - star_count, stars, bars - 1n, groups);
  }
}

function adjust_colors(colors, color_count) {
  // The original color index list needs to be processed so that each
  // index is in reference to the entire list of colors. Before processing
  // each subsequent index assumes the previous color was removed.

  let indexes = [];
  for (let i = 0; i < color_count; i++) {
    indexes.push(i);
  }

  let adjusted = [];
  for (let c of colors) {
    adjusted.push(indexes.splice(Number(c), 1)[0]);
  }
  return adjusted;
}

function extract(index, range_data, N, color_count) {
  index = BigInt(index);
  color_count = BigInt(color_count);
  N = BigInt(N);

  let K = range_data.segments;
  let max_index = range_data.max_index;
  let count = range_data.range;

  let bases = [range_data.partitions];
  for (let n = color_count; n > color_count - K; n--) {
    bases.push(n);
  }

  // The bases are arranged [partition base, color 1, color 2, ...]
  let [partition, ...colors] = extract_digits(index, bases);

  // Now we go from partition index to segment lengths.
  let segments = star_bars_unrank(partition, N - K, K - 1n);
  for (let i = 0; i < segments.length; i++) {
    segments[i] += 1;
  }

  return [segments, adjust_colors(colors, color_count)];
}

function circle_count(circle_slices, circle_segments, colors) {
  // First we count the ways we can distribute the slices among the segments
  // with each segment having at least 1 slice
  partitions = combinations(circle_slices - 1n, circle_segments - 1n);

  // Then how many ways we can color the segments uniquely
  colorings = permutations(colors, circle_segments);

  return [partitions, colorings];
}

function generate_ranges(slices, max_segments, colors) {
  let result = [];

  slices = BigInt(slices);
  max_segments = BigInt(max_segments);
  colors = BigInt(colors);

  let i = 0n;
  for (let K = 1n; K <= max_segments; K++) {
    let [partitions, colorings] = circle_count(slices, K, colors);
    let count = partitions * colorings;

    result.push({
      max_index: i + count,
      range: count,
      partitions: partitions,
      segments: K
    });

    i += count;
  }

  return result;
}

function index_to_circle(index, circle_data) {
  index = BigInt(index);

  let range_i = 0;
  while (index >= circle_data.ranges[range_i].max_index) {
    range_i += 1;
  }

  let range = circle_data.ranges[range_i];
  let offset = range.max_index - range.range;

  return extract(
    index - offset,
    range,
    circle_data.pieces,
    circle_data.colors.length
  );
}

function polar_to_xy(cx, cy, radius, angle_rad) {
  let x = cx + radius * Math.cos(angle_rad);
  let y = cy + radius * Math.sin(angle_rad);

  return [x, y];
}

function make_arc(x, y, radius, start_angle, end_angle) {
  let [startx, starty] = polar_to_xy(x, y, radius, end_angle);
  let [endx, endy] = polar_to_xy(x, y, radius, start_angle);

  let large_arc_flag = end_angle - start_angle > Math.PI ? 1 : 0;

  let move = `M ${startx},${starty} `;
  let arc = `A ${radius},${radius} 0 ${large_arc_flag} 0 ${endx},${endy}`;

  return move + arc;
}

function circle_to_svg(segments, colors, color_list) {
  let angles = [0.0];
  let total_segment = segments.reduce((a, x) => a + x, 0);
  let segment_start = 0;
  for (let s of segments) {
    segment_start += s;
    angles.push((segment_start / total_segment) * Math.PI * 2);
  }

  let paths = [];
  for (let i = 0; i < colors.length; i++) {
    let d = make_arc(0, 0, 100, angles[i], angles[i + 1]);
    let path = `<path d="${d}" fill="none" stroke="${
      color_list[colors[i]]
    }" stroke-width="30" />`;
    paths.push(path);
  }

  return `<svg width="100px" version="1.1" viewBox="-120 -120 240 240" xmlns="http://www.w3.org/2000/svg">${paths.join(
    ""
  )}</svg>`;
}

function generate_circles(mode) {
  comment.innerText = "";
  if (!validate_input()) {
    return;
  }

  let N = pieces.value;
  let P = segments.value;
  let color_list = colors.value.trim().split("\n");
  let C = color_list.length;

  let result = generate_ranges(N, P, C);
  let circles = {
    pieces: N,
    max_segments: P,
    colors: color_list,
    ranges: result
  };

  svg_area.innerHTML = "";

  comment.innerHTML = `Total circles possible: ${
    result[result.length - 1].max_index
  }`;

  if (mode == "random") {
    // TODO: Not sure how to generate random BigInt numbers outside of the Number range
    let rand_range;
    if (result[result.length - 1].max_index > BigInt(Number.MAX_SAFE_INTEGER)) {
      comment.innerHTML += `<br/>Notice: Due to some issues, we're only able to generate indexes up to ${Number.MAX_SAFE_INTEGER}`;
      rand_range = Number.MAX_SAFE_INTEGER;
    } else {
      rand_range = Number(result[result.length - 1].max_index);
    }

    for (let i = 0; i < parseInt(amount.value); i++) {
      let index = BigInt(Math.floor(Math.random() * rand_range));
      let [segments, colors] = index_to_circle(index, circles);
      svg_area.innerHTML += circle_to_svg(segments, colors, color_list);
    }
  } else if (mode == "range") {
    let max_val = result[result.length - 1].max_index;
    let start = BigInt(start_index.value);
    let stop = BigInt(stop_index.value);

    if (stop < start) {
      error.innerText = "Range start cannot be after stop.";
      return;
    }

    if (stop < 0 || stop >= max_val || start < 0 || start >= max_val) {
      error.innerText = "Start or stop outside of allowable circle indices";
      return;
    }

    for (let i = start; i <= stop; i++) {
      let [segments, colors] = index_to_circle(i, circles);
      svg_area.innerHTML += circle_to_svg(segments, colors, color_list);
    }
  } else if (mode == "single") {
    let max_val = result[result.length - 1].max_index;
    let i = BigInt(circle_index.value);

    if (i < 0 || i >= max_val) {
      error.innerText = "Index outside of allowable circle indices";
      return;
    }

    let [segments, colors] = index_to_circle(i, circles);
    svg_area.innerHTML += circle_to_svg(segments, colors, color_list);
  }
}

function validate_input() {
  let N = parseInt(pieces.value);
  let P = parseInt(segments.value);

  if (P > N) {
    error.innerText = "Segments cannot be greater than pieces count.";
    return false;
  }

  let split_colors = colors.value.trim().split("\n");
  for (let i = 0; i < split_colors.length; i++) {
    if (!split_colors[i].match(/^#[0-9a-fA-F]{6}$/)) {
      error.innerText = `Color ${split_colors[i]} doesn't match the pattern #123456`;
      return false;
    }
  }

  let C = split_colors.length;

  if (P > C) {
    error.innerText = "Segments cannot be greater than color count.";
    return false;
  }

  error.innerText = "";
  return true;
}

generate_rand.onclick = () => generate_circles("random");
generate_range.onclick = () => generate_circles("range");
generate_single.onclick = () => generate_circles("single");

