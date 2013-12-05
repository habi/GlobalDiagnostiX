<?xml version="1.0" encoding="UTF-8"?><!-- DWXMLSource="NEW_PROD-REV1-DEV.xsdat" -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Aptina Imaging <xsl:value-of select="sensor/@part_number"/>-<xsl:value-of select="sensor/@version_name"/></title>
</head>
<body>
  <div style="float:left;display:block;font-weight:normal;font-family:Geneva, Arial, Helvetica, sans-serif;">
	<h1 style="font-size:20px;line-height:20px;">
	<span style="vertical-align:super">
       <xsl:text>&#160;&#160;&#160;&#160;</xsl:text>Aptina Imaging<xsl:text>&#160;&#160;&#160;&#160;</xsl:text><xsl:value-of select="concat(sensor/@part_number,'&#160;&#160;')"/><xsl:value-of select="concat('&#160;&#160;',sensor/@version_name)"/>
	</span></h1>
	<pre style="font-size:12px;"><xsl:value-of select="sensor/copyright"/></pre>
	<pre style="font-size:12px;"><xsl:text>&lt;--</xsl:text><xsl:value-of select="sensor/revision"/><xsl:text>--&gt;</xsl:text></pre>
    <table>
	   <tr>
	      <td valign="top">
			<h2 style="font-size:16px;line-height:16px;">&#160;Chip Descriptor</h2>			
			<table border="1" cellspacing="1" cellpadding="1" style="font-size:11px;">  
				<tr><td bgcolor="#9acd32"><b>Name</b></td><td><xsl:value-of select="concat(sensor/@name, '&#160;')"/></td></tr><!-- need a white space at the end to display table column correctly -->	
				<tr><td bgcolor="#9acd32"><b>Part Number</b></td><td><xsl:value-of select="concat(sensor/@part_number, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Version</b></td><td><xsl:value-of select="concat(sensor/@version, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Version Name</b></td><td><xsl:value-of select="concat(sensor/@version_name, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Width</b></td><td><xsl:value-of select="concat(sensor/@width, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Height</b></td><td><xsl:value-of select="concat(sensor/@height, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Image Typ</b>e</td><td><xsl:value-of select="concat(sensor/@image_type, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Bits per Clock</b></td><td><xsl:value-of select="concat(sensor/@bits_per_clock, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Clocks per Pixel</b></td><td><xsl:value-of select="concat(sensor/@clocks_per_pixel, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Pixel Clock Polarity</b></td><td><xsl:value-of select="concat(sensor/@pixel_clock_polarity, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Full Width</b></td><td><xsl:value-of select="concat(sensor/@full_width, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Full Height</b></td><td><xsl:value-of select="concat(sensor/@full_height, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Reg Addr Size</b></td><td><xsl:value-of select="concat(sensor/@reg_addr_size, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Reg Data Size</b></td><td><xsl:value-of select="concat(sensor/@reg_data_size, '&#160;')"/></td></tr>
				<tr><td bgcolor="#9acd32"><b>Ship Base Address</b></td><td><xsl:value-of select="concat(sensor/@ship_base_address, '&#160;')"/></td></tr>
			</table><br /><br />
         </td>
		 <td><xsl:text>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</xsl:text></td>
		 <td rowspan="15" valign="top">
			<h2 style="font-size:16px;line-height:16px;">&#160;Address Spaces</h2>
			<table border="1" cellspacing="1" cellpadding="1" style="font-size:11px;" align="right">
			  <tr bgcolor="#9acd32">
				<th>Name</th>
				<th>Type</th>
				<th>Value</th>
				<th>Description</th>
			  </tr>
			  <xsl:for-each select="sensor/addr_spaces/space">
				  <tr>
					<td><a href="#{@name}"><xsl:value-of select="@name"/></a></td>
					<td><xsl:value-of select="@type"/></td>		
					<td><xsl:value-of select="@value"/></td>
					<td nowrap="nowrap"><xsl:value-of select="@desc"/></td>
				  </tr>
			  </xsl:for-each>	  
			</table><br /><br />		 
         </td>		 
		 <td><xsl:text>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</xsl:text></td>
		 <td rowspan="15" valign="top">
			<br /><br /><br />
			<table cellspacing="0" style="font-size:11px;" align="right">
			  <tr>
				<td nowrap="nowrap">Click the page name to jump to the beginning of a page.<br />(page anchors may not work in IE 6).<br /><br />Registers are ordered by address for 16-bit and 32-bit addresses.<br />A page of registers may not be contiguous.<br /></td>
			  </tr>	
			</table>
		  </td>
      </tr>
    </table><br /><br />
	
    <h2 style="font-size:16px;line-height:16px;">&#160;Register/Bitfield Definitions</h2>
    <p style="font-size:11px;line-height:11px;">&#160;Note that items displayed in <font color="#FF0000"><b>Red</b></font> indicate their contents are Confidential, items displayed in <font color="#000000"><b>Black</b></font> indicate their contents are NDA, and items displayed in <font color="#009933"><b>Green</b></font> indicate their contents are Public.</p>
	<table border="0" cellspacing="0" cellpadding="2" style="font-size:11px;">
 	<xsl:call-template name="Display_Reg_Header"/>
 	<xsl:call-template name="Display_Reg_Row">
		<xsl:with-param name="Reg_Nodes" select="sensor/registers/reg"/>
    </xsl:call-template>
    </table><br /><br />

	<h2 style="font-size:16px;line-height:16px;">&#160;Demo System</h2>
	<table border="1" cellspacing="0" style="font-size:11px;">
 	<xsl:call-template name="Display_Demo_System"/>	  
	</table> 
  	  
<br /></div>
</body>
</html>
</xsl:template>


<xsl:template name="Display_Reg_Header">
      <tr bgcolor="#9acd32" align="left">
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Register Name</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Address</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Type</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Span</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Mask</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">RW</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Default</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px" nowrap="nowrap">Data Type</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Minimum</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Maximum</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Volatile?</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Description</th>
        <th style="border:solid; border-color:#E0E0E0; border-width:1px">Detail</th>
      </tr>
</xsl:template>

<xsl:template name="Display_Reg_Row">
   <xsl:param name="Reg_Nodes"/>
   <xsl:for-each select="$Reg_Nodes">
      <xsl:choose>
         <xsl:when test="@confidential != ''">
			<xsl:choose>
				<xsl:when test="@confidential = 'Y'">
					<xsl:call-template name="Format_Red_Row"/>
				</xsl:when>
				<xsl:otherwise>
				   <xsl:call-template name="Format_Green_Row"/>
				</xsl:otherwise>
			</xsl:choose>			
		 </xsl:when>	 
		 <xsl:otherwise>
           <xsl:call-template name="Format_Black_Row"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:call-template name="Display_Bit_Row">
	     <xsl:with-param name="Bit_Nodes" select="bitfield"/>
      </xsl:call-template>
   </xsl:for-each>
</xsl:template>

<xsl:template name="Display_Bit_Row">
   <xsl:param name="Bit_Nodes"/>  
   <xsl:for-each select="$Bit_Nodes">
      <xsl:choose>
         <xsl:when test="@confidential != ''">
			<xsl:choose>
				<xsl:when test="@confidential = 'Y'">
					<xsl:call-template name="Format_Red_Bit_Row"/>
				</xsl:when>
				<xsl:otherwise>
				   <xsl:call-template name="Format_Green_Bit_Row"/>
				</xsl:otherwise>
			</xsl:choose>			
         </xsl:when>
         <xsl:otherwise>
           <xsl:call-template name="Format_Black_Bit_Row"/>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:for-each>
</xsl:template>

<xsl:template name="Format_Red_Row">
  <tr style="color:#FF0000;">
    <xsl:call-template name="Display_Reg_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Red_Bit_Row">
  <tr style="color:#FF0000; background-color:#FFFFFF">
    <xsl:call-template name="Display_Bit_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Black_Row">
  <tr style="color:#000000">
    <xsl:call-template name="Display_Reg_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Black_Bit_Row">
  <tr style="color:#000000">
    <xsl:call-template name="Display_Bit_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Green_Row">
  <tr style="color: #009933; background-color:#FFFFFF">
    <xsl:call-template name="Display_Reg_Cells"/>
  </tr>
</xsl:template>

<xsl:template name="Format_Green_Bit_Row">
  <tr style="color:#009933; background-color:#FFFFFF">
    <xsl:call-template name="Display_Bit_Cells"/>
  </tr>
</xsl:template>
	
<xsl:template name="Display_Reg_Cells">  
	<td><xsl:value-of select="@name"/></td>		
	<td><xsl:value-of select="@addr"/></td>
	<td><a name="{@space}"><xsl:value-of select="@space"/></a></td>
	<xsl:choose>
		<xsl:when test="@span != ''">
			<td><xsl:value-of select="@span"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td>1</td>
		</xsl:otherwise>
	</xsl:choose>
	<td><xsl:value-of select="@mask"/></td>
	<xsl:choose>
		<xsl:when test="@rw != ''">
			<td><xsl:value-of select="@rw"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td>RW</td>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@default != ''">
			<td><xsl:value-of select="@default"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td>0x0000</td>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@datatype != ''">
		    <td><xsl:value-of select="@datatype"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td>unsigned</td>
			   </xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@range != ''">
			<td nowrap="nowrap"><xsl:value-of select="substring-before(@range, ' ')"/></td>
			<td nowrap="nowrap"><xsl:value-of select="substring-after(@range, ' ')"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td nowrap="nowrap">0x0000</td>
			<td nowrap="nowrap">0x0000</td>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@volatile != ''">
			<td nowrap="nowrap"><xsl:value-of select="@volatile"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td>N</td>
		</xsl:otherwise>
	</xsl:choose>
	<td nowrap="nowrap"><xsl:value-of select="@display_name"/></td>
	<xsl:choose>
		<xsl:when test="detail != ''"> <!-- detail is a tag, not an attribute -->
			<td nowrap="nowrap"><xsl:value-of select="detail"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td><xsl:text>&#160;&#160;</xsl:text></td>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<xsl:template name="Display_Bit_Cells">
	<td><xsl:text>&#160;&#160;</xsl:text><xsl:value-of select="concat('&#160;&#160;&#160;&#160;&#160;&#160;',@name)"/></td>
	<td><xsl:text>&#160;&#160;</xsl:text></td>  
	<td><xsl:text>&#160;&#160;</xsl:text></td> 
	<td><xsl:text>&#160;&#160;</xsl:text></td>
	<td><xsl:value-of select="@mask"/></td>
	<xsl:choose>
		<xsl:when test="@rw != ''">
			<td><xsl:value-of select="@rw"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td>RW</td>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@default != ''">
			<td><xsl:value-of select="@default"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td> </td>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@datatype != ''">
			<td><xsl:value-of select="@datatype"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td>unsigned</td>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@range != ''">
			<td nowrap="nowrap"><xsl:value-of select="substring-before(@range, ' ')"/></td>
			<td nowrap="nowrap"><xsl:value-of select="substring-after(@range, ' ')"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td nowrap="nowrap">0x0000</td>
			<td nowrap="nowrap">0x0000</td>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="@volatile != ''">
			<td nowrap="nowrap"><xsl:value-of select="@volatile"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td><xsl:text>&#160;&#160;</xsl:text></td>
		</xsl:otherwise>
	</xsl:choose>
	<td nowrap="nowrap"><xsl:value-of select="@display_name"/></td>
	<xsl:choose>
		<xsl:when test="detail != ''">
			<td nowrap="nowrap"><xsl:value-of select="detail"/></td>
		</xsl:when>
		<xsl:otherwise>
			<td><xsl:text>&#160;&#160;</xsl:text></td>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template name="Display_Demo_System">	
	<tr bgcolor="#9acd32">
		<th><xsl:text>&#160;&#160;&#160;&#160;</xsl:text></th>
		<th>Register</th>
		<th>Name</th>
		<th>Serial</th>
		<th>Address</th>
		<th>Mask</th>
		<th>Value</th>
		<th>Timeout</th>
	</tr>
	<xsl:for-each select="sensor/demo_system/*">
	  <tr>
		<td><xsl:value-of select="name()"/></td>  <!-- get the currnet node name -->
		<xsl:choose>
			<xsl:when test="@reg != ''">
				<td nowrap="nowrap"><xsl:value-of select="@reg"/></td>
			</xsl:when>
			<xsl:otherwise>
				<td><xsl:text>&#160;&#160;</xsl:text></td>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="@name != ''">
				<td nowrap="nowrap"><xsl:value-of select="@name"/></td>
			</xsl:when>
			<xsl:otherwise>
				<td><xsl:text>&#160;&#160;</xsl:text></td>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="@serial != ''">
				<td nowrap="nowrap"><xsl:value-of select="@serial"/></td>
			</xsl:when>
			<xsl:otherwise>
				<td><xsl:text>&#160;&#160;</xsl:text></td>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="@addr != ''">
				<td nowrap="nowrap"><xsl:value-of select="@addr"/></td>
			</xsl:when>
			<xsl:otherwise>
				<td><xsl:text>&#160;&#160;</xsl:text></td>
			</xsl:otherwise>
		</xsl:choose>
		<td><xsl:value-of select="concat(@mask, '&#160;')"/></td>
		<td><xsl:value-of select="concat(@value, '&#160;')"/></td>
		<td><xsl:value-of select="concat(@timeout, '&#160;')"/></td>
	  </tr>
	</xsl:for-each>
</xsl:template>

</xsl:stylesheet>


