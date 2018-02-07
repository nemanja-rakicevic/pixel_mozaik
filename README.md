# Mozaik

Just a simple script to which you provide a photo, and it returns the same photo but as a mosaic of your favourite thing of the day.
Zoom in.

------

### Example
`python mozaik.py -i "Arnold.jpg" -g "pug"`


<table border=0px bgcolor="#FFF">
<!-- <caption>2x2 images in a table</caption> -->
<colgroup>
<col width="30%" />
<col width="5%" />
<col width="30%" />
</colgroup>
<tbody>
<tr>
<td align="center"><img src="original_images/Arnold2.jpg" alt="" /></td>
<td align="center"><img src="example_images/r.png" alt="" /></td>
<td align="center"><img src="example_images/Arnold2_mozaikd.jpg" alt="" /></td>
</tr>
<tr>
<td align="center"><img src="original_images/Godfather.jpg" alt=""  /></td>
<td align="center"><img src="example_images/r.png" alt="" /></td>
<td align="center"><img src="example_images/Godfather_mozaikd.jpg" alt=""  /></td>
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