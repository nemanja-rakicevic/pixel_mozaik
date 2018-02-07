# Mozaik

Just a simple script to which you provide a photo, and it returns the same photo but as a mosaic of your favourite thing of the day.

------

### Example
`python mozaik.py -i "Arnold.jpg" -g "pug"`

<!-- 

<img src="original_images/Arnold2.jpg" alt="Arnold" width=40% align='left'/> 
<img src="example_images/right_arrow.svg" alt="ra" width=5% align='center'/> 
<img src="example_images/Arnold2_mozaikd.jpg" alt="Arnold_mozaik" width=55% align='right'/> 


<img src="original_images/Godfather.jpg" alt="Arnold" width=40% align='left'/> 
<img src="example_images/right_arrow.svg" alt="ra" width=5% align='center'/>  
<img src="example_images/Godfather_mozaikd.jpg" alt="Arnold_mozaik" width=55% align='right'/> 
 -->



<table>
<!-- <caption>2x2 images in a table</caption> -->
<<!-- colgroup>
<col width="20%" />
<col width="1%" />
<col width="80%" />
</colgroup> -->
<tbody>
<tr class="Input">
<td align="right"><img src="original_images/Arnold2.jpg" alt="" /></td>
<td align="center"><img src="example_images/r.png" alt="" /></td>
<td align="left"><img src="example_images/Arnold2_mozaikd.jpg" alt="" /></td>
</tr>
<tr class="Output">
<td align="right"><img src="original_images/Godfather.jpg" alt="" /></td>
<td align="center"><img src="example_images/r.png" alt="" /></td>
<td align="left"><img src="example_images/Godfather_mozaikd.jpg" alt="" /></td>
</tr>
</tbody>
</table>



------

### Requirements
- python3
- requests
- numpy
- [pillow](https://pillow.readthedocs.io/en/latest/)
- [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Or just do:
`pip install -r reqirements.txt`