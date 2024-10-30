// https://github.com/2dprototype/tender-free

import "fs"
import "strings"
import "csv"
import "json"

var arr = []
var map = {}

fn(){
	data := embed("t.tsv")
	lines := strings.split(data, "\n")
	for i, l in lines {
		if i == 0 {
			continue
		}
		x := strings.split(l, "\t")
		c := strings.split(x[2], " ")
		d := ""
		if len(c) == 2 {
			d = strings.trim_space(c[1])
			d = strings.replace(d, ")", "", -1)
			d = strings.replace(d, "(", "", -1)
			c = strings.trim_space(c[0])
		} 
		else {
			c = strings.trim_space(x[2])
		}
		if c == "null" {
			continue
		}
		z := strings.trim_space(x[1])
		if map[c] == null {
			map[c] = [c, z, d]
		}
		else {
			if map[c][1] == "" {
				map[c][1] = z
			} else {
				map[c][1] = z
			}
			map[c][2] = d
		}
	}
}()

fn(){
	lines := csv.decode(embed("f.csv"))
	for i, l in lines {
		if i == 0 {
			continue
		}
		if map[l[1]] == null {
			map[l[1]] = [l[1], l[2], l[3]]
		}
		else {
			if map[l[1]][1] == "" {
				map[l[1]][1] = l[2]
			} else {
				map[l[1]][1] = l[2]
			}
			map[l[1]][2] = l[3]
		}
	}
}()


fn(){
	obj := json.decode(embed("data.json"))
	for k, v in obj.compounds {
		if map[k] == null {
			map[k] = [k, v, ""]
		}
		else {
			map[k][1] = v
		}
	}
}()

for m in map {
	arr.push(m)
}

debug(len(map))

fs.writefile("molecules.csv", csv.encode(arr))