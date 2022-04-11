let pieces = document.getElementById("pieces");
let segments = document.getElementById("segments");
let colors = document.getElementById("colors");
let generate = document.getElementById("generate");
let error = document.getElementById("error");
let svg_area = document.getElementById("svg_area");
let amount = document.getElementById("amount");
let comment = document.getElementById("comment");


window.onload = function() {

}

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

function circle_count(circle_slices, circle_segments, colors) {
  // First we count the ways we can distribute the slices among the segments
  // with each segment having at least 1 slice
  partitions = combinations(circle_slices - 1n, circle_segments - 1n);

  // Then how many ways we can color the segments uniquely
  colorings = permutations(colors, circle_segments);

  return [partitions, colorings];
}

function compress_digits(digits, bases) {
  // Turns a set of digits and their bases into a single number
  let n = 0n;
  for (let i = digits.length - 1; i >= 0; i--) {
    n = n * bases[i] + digits[i];
  }
  return n;
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

// Perm functions from https://codegolf.stackexchange.com/a/115024
function counter(s) {
  let counts = {};
  for (let i = 0; i < s.length; i++) {
    if (s[i] in counts) {
      counts[s[i]] += 1n;
    } else {
      counts[s[i]] = 1n;
    }
  }
  return counts;
}

function perm_count(s) {
  // Count the total number of permutations of sorted sequence `s`
  let n = factorial(BigInt(s.length));
  for (const [c, l] of Object.entries(counter(s))) {
    n /= factorial(BigInt(l));
  }
  return n;
}

function perm_rank(target, base) {
  // Determine the permutation rank of string `target`
  // given the rank zero permutation string `base`,
  // i.e., the chars in `base` are in lexicographic order.

  if (target.length < 2) {
    return 0n;
  }

  let total = 0n;
  let head = target[0];
  let newtarget = target.substring(1);

  for (let i = 0; i < base.length; i++) {
    const c = base[i];
    const newbase = base.substring(0, i) + base.substring(i + 1);
    if (c == head) {
      return total + perm_rank(newtarget, newbase);
    } else if (i != 0 && c == base[i - 1]) {
      continue;
    }
    total += perm_count(newbase);
  }
}

function perm_unrank(rank, base, head = "") {
  // Determine the permutation with given rank of the
  // rank zero permutation string `base`.
  rank = BigInt(rank);

  if (base.length < 2) {
    return head + base;
  }

  let total = 0n;
  for (let i = 0; i < base.length; i++) {
    const c = base[i];
    if (i < 1 || c != base[i - 1]) {
      let newbase = base.substring(0, i) + base.substring(i + 1);
      let newtotal = total + perm_count(newbase);
      if (newtotal > rank) {
        return perm_unrank(rank - total, newbase, head + c);
      }
      total = newtotal;
    }
  }
}

function adjust_colors(colors) {
  // The original color index list needs to be processed so that each
  // index is in reference to the entire list of colors. Before processing
  // each subsequent index assumes the previous color was removed.

  let adjusted = [];
  for (let i = 0; i < colors.length; i++) {
    let adjustment = 0n;
    for (let p = 0; p < i; p++) {
      if (colors[i] >= colors[p]) {
        adjustment += 1n;
      }
    }

    adjusted.push(colors[i] + adjustment);
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
  // console.log(`Extract: ${index} ${partition} ${colors}`);
  // Now we go from partition index to segment lengths. I think this part could be made more efficient
  let unranked = perm_unrank(
    partition,
    "*".repeat(Number(N - K)) + "|".repeat(Number(K - 1n))
  );
  let segments = [];
  for (const s of unranked.split("|")) {
    segments.push(s.length + 1);
  }

  return [segments, adjust_colors(colors)];
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
    let bases = [partitions];
    for (let n = colors; n > colors - K; n--) {
      bases.push(n);
    }

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

function generate_circles() {
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
    console.log(`err2 ${N} ${P} ${C}`);
    error.innerText = "Segments cannot be greater than color count.";
    return false;
  }

  error.innerText = "";
  return true;
}

generate.onclick = generate_circles;
