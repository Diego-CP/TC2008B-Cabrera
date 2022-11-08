// Emiliano Cabrera Ruiz - A01025453

// Just add this to an empty object and play, 
// all additional objects + components will be added from here

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

[RequireComponent(typeof(MeshFilter))]
public class meshGenerator : MonoBehaviour
{
    Mesh mesh;

    [SerializeField] Vector3[] vertices;
    Vector3 C;
    int[] triangles;

    GameObject[] vertexObjs;

    // Start is called before the first frame update
    void Start()
    {
        transform.position = new Vector3(0,0,0);

        gameObject.AddComponent<MeshRenderer>();

        vertexObjs = new GameObject[]
        {
            new GameObject("V1"),
            new GameObject("V2"),
            new GameObject("V3"),
            new GameObject("V4"),
            new GameObject("C")
        };

        foreach(var GO in vertexObjs)
        {
            GO.transform.parent = transform;
            var iconContent = EditorGUIUtility.IconContent("sv_icon_dot13_sml");
            EditorGUIUtility.SetIconForObject(GO, (Texture2D) iconContent.image);
        }
        
        C = new Vector3 (-1.812f,-6.824f,5.247f);

        this.transform.GetChild(0).transform.position = new Vector3 (-1.812f,-6.824f,7.152f);
        this.transform.GetChild(1).transform.position = new Vector3 (-3.462f,-6.824f,4.294f);
        this.transform.GetChild(2).transform.position = new Vector3 (-0.162f,-6.824f,4.294f);
        this.transform.GetChild(3).transform.position = new Vector3 (-1.812f,-4.129f,5.247f);
        this.transform.GetChild(4).transform.position = C;

        mesh = new Mesh();
        GetComponent<MeshFilter>().mesh = mesh;

        CreateShape();
        UpdateMesh();
        RotateThePyramid();
    }

    void CreateShape()
    {
        vertices = new Vector3[]
        {
            new Vector3 (-1.812f,-6.824f,7.152f),
            new Vector3 (-3.462f,-6.824f,4.294f),
            new Vector3 (-0.162f,-6.824f,4.294f),
            new Vector3 (-1.812f,-4.129f,5.247f)
            
        };

        triangles = new int[]
        {
            0,1,2,
            3,1,0,
            3,2,1,
            3,0,2
        };
    }

    void UpdateMesh()
    {
        mesh.Clear();

        mesh.vertices = vertices;
        mesh.triangles = triangles;

        mesh.RecalculateNormals();
    }

    void RotateThePyramid()
    {
        Vector3 V1 = this.transform.GetChild(0).transform.position;
        Vector3 V2 = this.transform.GetChild(1).transform.position;
        Vector3 V3 = this.transform.GetChild(2).transform.position;
        Vector3 V4 = this.transform.GetChild(3).transform.position;

        Vector3 C_V1 = TranslateTo(V1);
        Vector3 C_V2 = TranslateTo(V2);
        Vector3 C_V3 = TranslateTo(V3);
        Vector3 C_V4 = TranslateTo(V4);


        vertices = new Vector3[]
        {
            TranslateFrom(RotateOnY(C_V1,-15f)),
            TranslateFrom(RotateOnY(C_V2,-15f)),
            TranslateFrom(RotateOnY(C_V3,-15f)),
            TranslateFrom(RotateOnY(C_V4,-15f))
        };

        UpdateMesh();
    }

    Vector3 RotateOnY(Vector3 vertex, float deg)
    {
        float angle = deg * Mathf.Deg2Rad;
        float sin = Mathf.Sin(angle);
        float cos = Mathf.Cos(angle);

        float x = (vertex.x * cos) + (vertex.z * sin);
        float z = (vertex.z * cos) - (vertex.x * sin);


        return new Vector3(x, vertex.y, z);
    }

    Vector3 TranslateTo(Vector3 vertex)
    {
        return new Vector3(vertex.x - C.x, vertex.y - C.y, vertex.z - C.z);
    }

    Vector3 TranslateFrom(Vector3 vertex)
    {
        return new Vector3(vertex.x + C.x, vertex.y + C.y, vertex.z + C.z);
    }
}
